import gym
from gym import spaces
import numpy as np
import json

from .classes import AgentCar, Participant
from .functions import Helper, Logging
from .models import model_startingGrid, model_lap


class RaceSimulation(gym.Env):
    def __init__(self, config): # the passed "config" parameter is defined in the initialization of the environment (eg. notebook)
        #* Global config
        self.config = config

        #* Observation space
        # TODO: use the observation_space parameters from the main config -> self.observation_space = config['observation_space']
        self.low = np.array([1, 0], dtype=np.int)
        self.high = np.array([config['RACESIMULATION']['RACE_GRIDSIZE'], 100], dtype=np.int)
        self.observation_space = spaces.Box(self.low, self.high, dtype=np.int)
        
        #* Action space
        # TODO: use the Action space parameters from the main config
        self.action_space = spaces.Discrete(4)

        #* Agent car
        self.agent_car = AgentCar(Participant(
            "Agent", # participant_id
            config['RACESIMULATION']['RACE_INITFUELMASS'], # init fuel mass
            0, # this is overridden when initializing the actual race_grid!
        ))

        #* (Lap) Models
        self.model_lap = model_lap(config)

        #* Static parameters for the race simulation
        self.race_length = config['RACESIMULATION']['RACE_LENGTH'] # length of the race
        self.race_gridSize = config['RACESIMULATION']['RACE_GRIDSIZE'] # amount of participants
        self.race_lap = 1 # current lap of the race
        self.race_grid = [] # array of participant instances



    #
    # * this function (re)initializes the simulation. 
    #
    def reset(self):
        # logging
        Helper.global_logging(self.config['LOGGING'], "ENVIRONMENT", "\n[bold red]Initializing simulation...[/bold red]\n")
        

        # * resetting simulation
        self.race_length = self.config['RACESIMULATION']['RACE_LENGTH'] # length of the race
        self.race_gridSize = self.config['RACESIMULATION']['RACE_GRIDSIZE'] # amount of participants
        self.race_lap = 1 # current lap of the race
        self.race_grid = [] # array of participant instances
        self.model_lap = model_lap(self.config)
        self.agent_car = AgentCar(Participant(
            "Agent", # participant_id
            self.config['RACESIMULATION']['RACE_INITFUELMASS'], # init fuel mass
            0, # this is overridden when initializing the actual race_grid!
        ))


        # * generating starting grid
        self.race_grid = model_startingGrid.gen_startingGrid(self.config, self.agent_car, self.race_gridSize)

        # logging starting grid
        if self.config['LOGGING']['SIMULATION']['GRID_GENERATION']:
            Logging.log_starting_grid(self.race_lap, self.race_grid)


        # * generating accidents and code60 phases
        # TODO: implement generating accidents and code60 phases
        # ! this is not done yet!!!


        # * generating and returning initial observation
        obs = self.observe()
        return obs


    #
    # * this function simulates each time step
    #
    def step(self, action):
        # logging
        Helper.global_logging(self.config['LOGGING']['SIMULATION'], "LAP", "\nSimulating Lap [bold]#{}[/bold]".format(self.race_lap))

        
        # * 1 - perform the action chosen by the agent
        # ? should this really be done before everything else?
        agent_action = self.agent_car.take_action(action)


        # * 2 - simulating laps for all participants      
        self.model_lap.simulate_lap(self.race_lap, self.race_grid)


        # logging table of all participant timings for this lap
        if self.config['LOGGING']['SIMULATION']['GRID_POSITIONS']:
            Logging.log_lap_timings(self.race_lap, self.race_grid)


        # increasing lap count
        # ? is this the right place??
        self.race_lap += 1


        # * 3 - Generate required return values
        obs = self.observe() # getting current state of environment
        reward = self.agent_car.calc_reward() # calculating reward based on last action


        # logging agent action
        Helper.global_logging(self.config['LOGGING']['AGENT'], "ACTIONS", "[yellow]Agent took action {}, got {} in reward and moved {} positions[/yellow]\n".format(agent_action, reward, (self.agent_car.car.lastLap_position - self.agent_car.car.race_position) ))


        # checking if episode is terminal
        done = self.is_done() 


        # * returning required fields for this step
        return obs, reward, done, {}


    #
    # * this function creates the observation object for the agent
    #
    # TODO: use observation fields defined in global config
    def observe(self):
        # * read and return observation
        # ? currently "race_position" and "tire age"
        #return (int(self.agent_car.car[self.config['observation_fields'][0]]), int(self.agent_car.car[self.config['observation_fields'][1]]))
        
        return (int(self.agent_car.car.race_position), int(self.agent_car.car.car_tireDeg))


    #
    # * this function checks if a terminal state is achieved
    #
    def is_done(self):
        # * check if all laps have been simulated
        if self.race_lap > self.race_length or self.agent_car.car.is_retired:
            Helper.global_logging(self.config['LOGGING'], "ENVIRONMENT", "[bold red]Simulation finished after {} lap(s)[/bold red]\n".format(self.race_lap-1))
            
            for idx_sector, participant in enumerate(self.race_grid):
                with open('./logs/'+participant.participant_id+'.json', 'w') as fout:
                    json.dump(participant.log, fout)
            return True
        
        # * otherwise, keep simulating the race
        else:
            return False


    #
    # * this function is mandatory, but not used
    #
    def render(self, mode):
        return None