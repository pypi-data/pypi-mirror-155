from .sector import Sector


class Track:
    def __init__(self,track_id):
        self.track_id = track_id
        self.sectors = [
            Sector({
                "sector_id": "S1",# as of official NLS document
                "sector_length": 2745.6,# as of official NLS document
                "base_time": 66.019,
                "timeLoss_fuelMass": 0.03,
                "timeLoss_tireDeg": 0.09,
                "wear_fuelCon": 1,
                "wear_tireDeg": 1.5,
                "factor_overtaking": 3,
                "variance_min": 0.6,
                "variance_max": 1.8,
                "prob_code60": 0.0
            }),

            Sector({
                "sector_id": "S2",# as of official NLS document
                "sector_length": 3003.9,# as of official NLS document
                "base_time": 63.468,
                "timeLoss_fuelMass": 0.035,
                "timeLoss_tireDeg": 0.05,
                "wear_fuelCon": 1,
                "wear_tireDeg": 1.2,
                "factor_overtaking": 3,
                "variance_min": 1.4,
                "variance_max": 2.9,
                "prob_code60": 0.07235
            }),

            Sector({
                "sector_id": "S3",# as of official NLS document
                "sector_length": 6002.5,# as of official NLS document
                "base_time": 117.133,
                "timeLoss_fuelMass": 0.06,
                "timeLoss_tireDeg": 0.08,
                "wear_fuelCon": 1,
                "wear_tireDeg": 3.2,
                "factor_overtaking": 3,
                "variance_min": 3.7,
                "variance_max": 4.8,
                "prob_code60": 0.17122
            }),

            Sector({
                "sector_id": "S4",# as of official NLS document
                "sector_length": 9409.4,# as of official NLS document
                "base_time": 183.532,
                "timeLoss_fuelMass": 0.08,
                "timeLoss_tireDeg": 0.12,
                "wear_fuelCon": 1,
                "wear_tireDeg": 4,
                "factor_overtaking": 3,
                "variance_min": 8.2,
                "variance_max": 9.9,
                "prob_code60": 0.19333
            }),

            Sector({
                "sector_id": "S5",# as of official NLS document
                "sector_length": 3196.6,# as of official NLS document
                "base_time": 48.829 ,
                "timeLoss_fuelMass": 0.01,
                "timeLoss_tireDeg": 0.07,
                "wear_fuelCon": 1,
                "wear_tireDeg": 0.8,
                "factor_overtaking": 3,
                "variance_min": 0.5,
                "variance_max": 1.7,
                "prob_code60": 0.09285
            }),
        ]

        self.code60_phases = []

"""
    def calc_baseLapTime(self,participant,prob):
        lapTime_obj = {
            "base_lapTime": 0,
            "timeLoss_tireDeg": 0,
            "timeLoss_fuelMass": 0,
            "timeLoss_variability": 0
        }

        # iterating over all sectors
        for sector in self.sectors:
            # logging
            if config.getboolean('debug','sector_fuelMass') | config.getboolean('debug','sector_tireDeg'):
                print(sector.sector_id)

            # calling sector_time function
            sectorTime_obj = sector.calc_sectorTime(participant,self.code60_phases)

            # adding results to lapTime_obj
            lapTime_obj["base_lapTime"] += sectorTime_obj["base_sectorTime"]
            lapTime_obj["timeLoss_tireDeg"] += sectorTime_obj["timeLoss_tireDeg"]
            lapTime_obj["timeLoss_fuelMass"] += sectorTime_obj["timeLoss_fuelMass"]
            lapTime_obj["timeLoss_variability"] += sectorTime_obj["timeLoss_variability"]

        

        return lapTime_obj


    def calc_lapFuelLoss(self,participant):
        fuel_loss = 0
        for sector in self.sectors:
            fuel_loss += sector.calc_sectorFuelLoss(participant)

        return fuel_loss

    def calc_lapTireDeg(self,participant):
        tire_deg = 0
        for sector in self.sectors:
            tire_deg += sector.calc_sectorTireDeg(participant)

        return tire_deg



"""