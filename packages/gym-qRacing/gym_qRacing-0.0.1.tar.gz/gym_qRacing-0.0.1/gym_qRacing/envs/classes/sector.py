import math
import random


class Sector:
    def __init__(self, sector_params):
        self.sector_id = sector_params["sector_id"] # identifier of this sector
        self.base_time = sector_params["base_time"] # best possible time (in sec) for car with optimal driver+fuel+tire parameters
        
        self.timeLoss_tireDeg = sector_params["timeLoss_tireDeg"]
        self.timeLoss_fuelMass = sector_params["timeLoss_fuelMass"]

        self.variance_min = sector_params["variance_min"]
        self.variance_max = sector_params["variance_max"]

        self.wear_fuelCon = sector_params["wear_fuelCon"] # amount of fuel burned in this sector
        self.wear_tireDeg = sector_params["wear_tireDeg"] # amount tire degregation in this sector

        self.factor_overtaking = sector_params["factor_overtaking"] # minimum distance between cars to overtake in this sector
        self.prob_code60 = sector_params["prob_code60"]

        self.code60_phases = {} # ! not implemented yet! Should have entry for each phase with start+end (comes from failed overtakes)
        
        # ! not implemented yet!
        #self.code60_timeLoss = sector_params["code60_timeLoss"] 


"""
    def calc_sectorTime(self, participant, code60_phases): 
        # calculating base sector time for participant, excluding any probabilistic factors

        timeLoss_tireDeg = self.calc_timeLoss_tireDeg(participant)
        timeLoss_fuelMass = self.calc_timeLoss_fuelMass(participant)
        timeLoss_variability = self.calc_timeLoss_variability(participant)

        if [self.sector_id, participant.race_lap] in code60_phases:
            timeLoss_code60 = 30
        else:
            timeLoss_code60 = 0 

        base_sectorTime = self.base_time + timeLoss_tireDeg + timeLoss_fuelMass + timeLoss_variability + timeLoss_code60
        
        # calculating probabilistic factors (eg. lap time variations)
        #prob_sectorTime = base_sectorTime + prob.calc_lapTimeVariation(participant)

        #sector_time = base_sectorTime + prob_sectorTime
        
        return {
            "base_sectorTime": base_sectorTime,
            "timeLoss_tireDeg": timeLoss_tireDeg,
            "timeLoss_fuelMass": timeLoss_fuelMass,
            "timeLoss_variability": timeLoss_variability
        }


    def calc_timeLoss_fuelMass(self, participant):
        
        # penalty_fuelMass(fuel_amount) = sector_factor * fuel_amount + empty_tank_penalty
        sector_factor = self.timeLoss_fuelMass * 0.4 
        fuel_amount = participant.car_fuelMass
        empty_tank_penalty = 0 # ? no fuel mass = no timeLoss due to fuel mass
        timeLoss_fuelMass = sector_factor * fuel_amount + empty_tank_penalty

        if config.getboolean('debug', 'sector_fuelMass'):
            print("timeLoss fuel_mass: {:9.2f}s \n".format(timeLoss_fuelMass))
        
        return timeLoss_fuelMass


    def calc_timeLoss_tireDeg(self, participant):
        
        # penalty_tireDeg(tire_age) = deg_factor_1 * log(deg_factor_2 * tire_age + target_lap)
        deg_factor_1 = self.timeLoss_tireDeg # amount of impact by tireDeg on sector time 
        deg_factor_2 = 4 # coefficent for tire deg 
        tire_age = participant.stint_length
        target_lap = 1 # lap to calculate timeLoss for. 1 = next lap, wheras 0 = current ("past") lap
        timeLoss_tireDeg = deg_factor_2 * math.log(deg_factor_1 * tire_age + target_lap)

        if config.getboolean('debug', 'sector_tireDeg'):
            print("timeLoss tire_deg: {:10.2f}s".format(timeLoss_tireDeg))
        
        return timeLoss_tireDeg


    def calc_timeLoss_variability(self, participant):
        timeLoss_variability = random.uniform(self.variance_min, self.variance_max) 

        # !!! enabling the training
        if participant.participant_id != "Agent":
            timeLoss_variability += 1

        return timeLoss_variability






    def calc_sectorFuelLoss(self, participant):
        fuel_loss = self.wear_fuelCon * -1
        return fuel_loss

    def calc_sectorTireDeg(self, participant):
        tire_deg = self.wear_tireDeg
        return tire_deg

    def calc_sectorOvertake(self, race_grid, participant):
        overtake = False

        # calculate if an overtake should take place
        # should use participant.race_distanceFront to determine the distance between cars and self.factor_overtaking if overtake is possible
        # improved model also should implement probabilistic factor

        return overtake

"""