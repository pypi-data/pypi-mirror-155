from .participant import Participant


class AgentCar(Participant):
    def __init__(self, participant):
        self.participant_id = participant.participant_id
        self.car = participant

    #
    # * this function simulates the action chosen by the agent
    #
    def take_action(self, action):
        if action == 0:
            self.car.next_pitStop = {
                "amount": 4
            }
        if action == 1:
            self.car.next_pitStop = {
                "amount": 6
            }
        if action == 2:
            self.car.next_pitStop = {
                "amount": 8
            }
        elif action == 3:
            self.car.next_pitStop = None

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
        if pos_change > 0: # for lost positions
            reward = -1 * pos_change
        if pos_change < 0: # for gained positions
            reward = -1 * pos_change
        if self.car.race_position < 6: # if the agent is within the top 5
            reward += 3

        return reward
