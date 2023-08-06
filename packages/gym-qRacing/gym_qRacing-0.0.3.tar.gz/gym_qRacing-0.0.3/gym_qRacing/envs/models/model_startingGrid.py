from ..functions import Helper
from ..classes import Participant

class model_startingGrid():
    #
    # * this function generates participants to fill the race_grid
    #
    # TODO: implement generation of starting grid
    @staticmethod
    def gen_startingGrid(config, agent_car, grid_size):
        # initializing variables
        race_grid = []
        current_last_gridPosition = 0

        # * iterate over grid_size and generate random participants
        for i in range(1, (grid_size)):

            # add new instance of participant to race_grid list
            race_grid.append(Participant(
                "Car {}".format(i), # participant_id
                config['RACESIMULATION']['RACE_INITFUELMASS'], # init fuel mass
                i, # initial race position (on init = grid position)
            ))

            # keeping track of the last grid position assigned
            current_last_gridPosition = i


        # * adding agent_car to race grid
        race_grid.append(agent_car.car)

        # assigning the correct race position to the agent car
        agent_car.car.race_position = current_last_gridPosition+1 

        return race_grid

