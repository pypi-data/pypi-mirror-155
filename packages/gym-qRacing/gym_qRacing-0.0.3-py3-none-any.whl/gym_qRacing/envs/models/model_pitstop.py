class Model_PitStop(object):
    def __init__(self, config):
        self.travelTime_in = config['MODELS']['PITSTOP']['TIMELOSS_TRAVELIN']
        self.travelTime_out = config['MODELS']['PITSTOP']['TIMELOSS_TRAVELOUT']
        
        self.standingTime_free = config['MODELS']['PITSTOP']['STANDINGTIME_FREE']

        # ! this is not implemented yet and provides a empty list
        self.standingTime_regulation = config['MODELS']['PITSTOP']['STANDINGTIME_REGULATION']

        self.init_fuelMass = config['RACESIMULATION']['RACE_INITFUELMASS']



    @staticmethod
    def sim_pitStop(participant, action):
        # TODO: integrate mandatory standing times from NLS regulation

        # @ travelTime_in
        # @ travelTime_out
        # @ serviceTime_free
        # @ serviceTime_regulation


        # timeLoss_pitStop = travelTime_in + travelTime_out + ? serviceTime_free : serviceTime_regulation


        # return timeLoss_pitStop

        #print(participant.participant_id, " is pitting!")

        participant.car_tireDeg = 0
        participant.car_fuelMass = action * 10.0 #! this should not be static!!!!
        return False 

