from .participant import Participant


class AgentCar(Participant):
    def __init__(self, participant):
        self.participant_id = participant.participant_id
        self.car = participant
        self.current_action = 0

    #
    # * this function simulates the action chosen by the agent
    #
    def take_action(self, action, race_lap):

        if action == 0:
            self.car.car_pitStops.append([race_lap, 4])
        if action == 1:
            self.car.car_pitStops.append([race_lap, 6])
        if action == 2:
            self.car.car_pitStops.append([race_lap, 8])
        elif action == 3:
            self.car.next_pitStop = None


        #self.current_action = action
        return action


    #
    # * this function calculates the reward
    #
    def calc_reward(self):
        # TODO: make this controlable from the environment setup level
        # TODO: implement wandb logging to keep track of experiments

        # initializing variables
        reward = 0 # initial reward
        pos_change = self.car.race_position - self.car.lastLap_position # position change this lap


        #* assigning reward based on position change
        """
        if pos_change > 0: # for lost positions
            reward = -1 * pos_change
        if pos_change < 0: # for gained positions
            reward = -1 * pos_change
        if self.car.race_position < 6: # if the agent is within the top 5
            reward += 3
        """

        if self.car.car_tireDeg > 80:
            reward -= 1

        if self.car.race_position < 8:
            reward += 1

        if self.car.is_retired:
            reward = -10

        reward -= 0.1 * len(self.car.car_pitStops)

        return reward
