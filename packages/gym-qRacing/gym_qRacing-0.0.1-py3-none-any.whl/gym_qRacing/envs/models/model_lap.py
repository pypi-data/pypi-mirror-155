from ..functions import Helper, Logging
from ..models.model_car import model_car
from ..models.model_overtaking import model_overtaking
from ..classes import Track

from mlflow import log_metric, log_param

class model_lap():
    def __init__(self, config):
        self.config = config
        self.race_track = Track("Nordschleife") # creating instance of the race track


    #
    # * this function simulates a lap for all participants
    #
    # @race_lap:int -> the current lap of the race
    # @race_grid:[Participant] -> A list of Participant() instances, representing all cars in the race
    #
    # @return race_grid:[Participant] -> A updated list of Participant() instances, representing the new order of the grid
    #
    # TODO: integrate the "update_grid" + "update_wear" functions so they are called after each sector
    def simulate_lap(self, race_lap, race_grid):

        # * iterating over all sectors of the race track
        for idx_sector, sector in enumerate(self.race_track.sectors):

            # * iterating over all participants in this sector
            # TODO: apply models to participant (overtakes, failures/accidents etc.)
            for idx_participant, participant in enumerate(race_grid):     

                #* if its the last sector, decide if participant is pitting
                if (idx_sector+1) == len(self.race_track.sectors):
                    is_pitting = participant.decide_pitStop(race_lap)
                else:
                    is_pitting = False

                #* if its the first sector, check if participant was pitting last lap
                # ! implement time penalty for 1st sector after pitting!

                # * calculating the sector time for a participant in this specific sector, using a time-adjustment approach
                # calculate sector time
                sector_time = self.calc_sectorTime(participant, sector, race_lap, idx_sector, is_pitting)

                # add sector time to the current lap time
                participant.update_lapTime(sector_time)


                # * handling participant wear for this sector
                # calculate wear
                fuelCon = model_car.calc_fuelConsumption(sector, participant)
                tireDeg = model_car.calc_tireDeg(sector, participant)

                # update wear 
                participant.update_wear(tireDeg, fuelCon) 


                #log_metric(participant.participant_id+"_"+sector.sector_id, sector_time)

                # * add information to participant log dict
                participant.update_log_sector({
                    "race_lap": race_lap,
                    "sector_id": sector.sector_id,
                    "sector_data": {
                        "sector_time": sector_time,
                        "wear_tireDeg": tireDeg,
                        "wear_fuelCon": fuelCon,
                    }
                })



            # * updating race positions
            # TODO: calculate new race positions
            # ! this is not implemented yet!!!
            # ? not possible if active code60 phase!
            race_grid = model_overtaking.calc_positionChanges(sector, race_grid)
                    

            # * determine pit stops
            # TODO: determine pit stops
            # ! this is not implemented yet!!!
            # ? only for last sector!
            # ? how should pit stop decisions be done for other participants?


        #* returning updated grid
        return race_grid


    #
    # * this function calculates the lap time for a single participant
    #
    def calc_sectorTime(self, participant, sector, race_lap, sector_id, is_pitting):
        sector_time = 0.0

        # * deterministic time adjustments
        penalty_fuelMass = model_car.calc_timeLoss_fuelMass(participant, sector)
        penalty_tireDeg = model_car.calc_timeLoss_tireDeg(participant, sector)


        # * probabilistic time adjustments

        # race start
        # TODO: add race start model
        # ! this is not implemented yet!!!
        penalty_raceStart = 0
        if race_lap == 1 and sector_id == 0:
            penalty_raceStart = self.config['MODELS']['RACESTART']['TIMELOSS_BASE'] # TODO: this has to be implemented as empiric model!

        # traffic
        # TODO: add time variance model
        # ! this is not implemented yet!!!
        penalty_trafficImpairment = model_overtaking.calc_trafficImpairment() * 0.5

        # code60 + accidents
        # TODO: apply possible code60 phases
        # ! this is not implemented yet!!!
        # ? -> check if sector has an active phase and apply time penalty

        # pit stops
        # TODO: use real pit stop model!!!
        # ? only for last sector (+ first of following lap) and only, if participant chose to stop!
        if is_pitting:

            # check if its the inlap or outlap of the pitstop
            if race_lap == participant.car_pitStops[len(participant.car_pitStops)-1]:
                # its the inlap, apply timeLoss_travelIn and standingTime
                penalty_pitStop = self.config['MODELS']['PITSTOP']['TIMELOSS_TRAVELIN'] + self.config['MODELS']['PITSTOP']['STANDINGTIME_FREE']
            else:
                # its the outlap, only apply travelOutTime
                penalty_pitStop = self.config['MODELS']['PITSTOP']['TIMELOSS_TRAVELOUT']
        else:
            penalty_pitStop = 0


        #* the actual sector time calculation
        # ? Tlap = Σ (Tsector base + Ptire deg + Pfuel mass) + Ptraffic + Ppit stop + Prace start
        sector_time = (sector.base_time + penalty_fuelMass + penalty_tireDeg) + penalty_raceStart + penalty_trafficImpairment + penalty_pitStop


        return sector_time


