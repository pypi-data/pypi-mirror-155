from ..functions import Helper
import random
from rich import print

class model_overtaking():
    def __init__(self, config):
        self.config = config


    #
    # * this function calculates possible position changes
    # ? should be called after each sector!
    # TODO: implement the actual logic + algorithm
    #
    @staticmethod
    def calc_positionChanges(sector, race_grid, config):
        #
        # ? changes are not possible if active Code60 phase! This has to be accounted for!

        if config['LOGGING']['SIMULATION']['SECTOR']:
            print("\nSimulating sector {}".format(sector.sector_id))

        # compare race_time between 2 participants and change position in race_grid list
        # while position_changes (in this loop) > 0
        while True:
            position_changes = 0
            for idx_participant, participant in enumerate(race_grid):
                # skip 1st place
                if idx_participant == 0:
                    continue
                

                # check if position change should take place
                # TODO: implement overtake model to introduce probability
                if participant.race_time < race_grid[idx_participant-1].race_time: # the participant in this iteration is faster than the car in front -> move up 1 place
                    

                    # storing the participant one place up temporarly
                    temp_participant_overtaken = race_grid[idx_participant-1]

                    # overriding the overtaken participant in the race_grid
                    race_grid[idx_participant-1] = participant

                    # storing the overtaken participant one place down
                    race_grid[idx_participant] = temp_participant_overtaken

                    # increasing position_changes to signal a change has occured
                    position_changes += 1

                    # updating race_position
                    race_grid[idx_participant-1].race_position = idx_participant
                    race_grid[idx_participant].race_position = idx_participant+1

                    # logging
                    if config['LOGGING']['SIMULATION']['OVERTAKES']:
                        print("{} has overtaken {} for position #{}".format(participant.participant_id, race_grid[idx_participant].participant_id, idx_participant))



                # updating race position for each participant
                # ! this should only be done for the LAST sector of a lap!!!
                participant.lastLap_position = participant.race_position

            
            # if no more changes took place, everything is sorted and the loop can be left
            if position_changes < 1:
                break

        return race_grid


    #
    # * this function calculates a time penalty for traffic impairment
    # TODO: implement the actual logic + algorithm
    #
    @staticmethod
    def calc_trafficImpairment():
        # ! this is currently a placeholder!!!

        return random.randint(1,9)