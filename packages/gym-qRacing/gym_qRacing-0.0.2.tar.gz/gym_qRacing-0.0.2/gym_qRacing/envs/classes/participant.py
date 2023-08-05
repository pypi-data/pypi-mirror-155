from rich.console import Console
console = Console()

class Participant:
    def __init__(self, participant_id, car_fuelMass, race_position):
        self.participant_id = participant_id
        
        # * car parameters
        self.car_fuelMass = car_fuelMass
        self.car_tireDeg = 0
        self.car_pitStops = []


        # * race parameters
        self.race_time = 0
        self.race_position = race_position

        self.lastLap_time = 0
        self.lastLap_position = race_position

        self.delta_front = 0
        self.delta_back = 0


        # * status flags
        self.next_pitStop = None
        self.is_retired = False


        # * logging
        self.log = {
            "laps": {}
        }

        # structure of log dict:
        """ 
        self.log = {
            "laps": {
                   1: {                                                                                                                                       
                       'lap_time': 0.0,                                                                                                                       
                       'sectors': {                                                                                                                           
                           'S1': {'sector_time': 66.019, 'wear_tireDeg': 0, 'wear_fuelCon': 0},                                                               
                           'S2': {'sector_time': 63.468, 'wear_tireDeg': 0, 'wear_fuelCon': 0},                                                               
                           'S3': {'sector_time': 117.133, 'wear_tireDeg': 0, 'wear_fuelCon': 0},                                                              
                           'S4': {'sector_time': 183.532, 'wear_tireDeg': 0, 'wear_fuelCon': 0},                                                              
                           'S5': {'sector_time': 48.829, 'wear_tireDeg': 0, 'wear_fuelCon': 0}                                                                
                       },
                       'wear_tireDeg': 0, 
                       'wear_fuelCon': 0                                                                                                                               
                   }  
            }
        }
        """


    #
    # * this functions updates the lap_time and race_time for the participant
    #
    # TODO: implement handling of last sector and start of next lap
    def update_lapTime(self, sector_time):

        # updating last lap time
        self.lastLap_time += sector_time

        # updating race_time
        self.race_time += sector_time

        # TODO: also update lap_time for log dict!



    #
    # * this functions updates the wear for the participant
    #
    def update_wear(self, tire_deg, fuel_con):
        self.car_tireDeg += tire_deg
        self.car_fuelMass -= fuel_con

        #! this must lead to DNF!
        if self.car_tireDeg >= 100:
            #print("too high!")
            self.car_tireDeg = 100

        #! this must lead to DNF!
        if self.car_fuelMass < 1:
            #print("too high!")
            self.car_fuelMass = 1

    #
    # * this functions decides if the participant is pitting
    #
    def decide_pitStop(self, current_raceLap):
        if self.car_fuelMass < 30 or self.car_tireDeg > 80:
            self.car_pitStops.append(current_raceLap)
            return True
        else:
            return False


    def update_log_sector(self, log_dict):

        # * check if lap key exists
        if log_dict['race_lap'] not in self.log['laps']:
            # * create lap dict!
            self.log['laps'][log_dict['race_lap']] = {
                "lap_time": 0.0,
                "sectors": {},
                'wear_tireDeg': 0.0, 
                'wear_fuelCon': 0.0 
            }


        # * check if sector key exists
        if log_dict['sector_id'] not in self.log['laps'][log_dict['race_lap']]['sectors']:
            # * create sector dict!
            self.log['laps'][log_dict['race_lap']]['sectors'][log_dict['sector_id']] = log_dict['sector_data']

            # update lap time
            self.log['laps'][log_dict['race_lap']]['lap_time'] = self.log['laps'][log_dict['race_lap']]['lap_time'] + log_dict['sector_data']['sector_time']

            # update total wear for this lap
            self.log['laps'][log_dict['race_lap']]['wear_tireDeg'] = self.log['laps'][log_dict['race_lap']]['wear_tireDeg'] + log_dict['sector_data']['wear_tireDeg']
            self.log['laps'][log_dict['race_lap']]['wear_fuelCon'] = self.log['laps'][log_dict['race_lap']]['wear_fuelCon'] + log_dict['sector_data']['wear_fuelCon']


        #print(self.participant_id)
        #console.log(self.log)




"""

    def calc_lapTime(self, track, prob):

        # calculating base_lapTime
        lap_time_obj = track.calc_baseLapTime(self, prob)
        lap_time = lap_time_obj["base_lapTime"]
        timeLoss_tireDeg = lap_time_obj["timeLoss_tireDeg"]
        timeLoss_fuelMass = lap_time_obj["timeLoss_fuelMass"]
        timeLoss_variability = lap_time_obj["timeLoss_variability"]


        # calculating fuel_loss
        fuel_loss = track.calc_lapFuelLoss(self)

        # calculating tire_deg
        tire_deg = track.calc_lapTireDeg(self)


        # simulating pit stop
        
        if self.is_pitting:
            # initializing and simulating pitstop
            simulated_pit_stop = Pitstop(self.race_lap, self.pit_refuelAmount)
            simulated_pit_stop.simulate_pitStop(self)

            # adding pit stop time to lap_time
            lap_time += simulated_pit_stop.service_time

            # add pitstop to car_pitStops
            self.car_pitStops.append(simulated_pit_stop) # !!! this does not work for some reason! List keeps being empty
        

        # simulating race start time loss
        if self.race_lap == 0:
            # add time loss for acceleration to race pace on race start
            lap_time += config.getfloat('race_simulation', 'race_timeLossStart')


        # printing debug info
        if config.getboolean('debug', 'lap_participant_info'):
            print("\n#{} (+{:1.2f}s) - {}".format(self.race_position, self.race_distanceFront, self.participant_id))

            if config.getboolean('debug', 'lap_participant_raceTime'):
                print("RaceTime: {:1.2f}s".format(self.race_time))
            if config.getboolean('debug', 'lap_participant_lapTime'):
                print("LapTime: {:2.2f}s (last: {:1.2f}s)".format(lap_time, self.race_lastLapTime))
            if config.getboolean('debug', 'lap_participant_tireDeg'):
                print("FuelLoad: {:1.2f}L ({:1.2f}L) -> +{:1.2f}s".format(self.car_fuelMass, fuel_loss, timeLoss_fuelMass))
            if config.getboolean('debug', 'lap_participant_fuelMass'):
                print("TireDeg: {:3.2f}% (+{:1.2f}%) -> +{:1.2f}s".format(self.car_tireDeg, tire_deg, timeLoss_tireDeg))
            if config.getboolean('debug', 'lap_participant_variability'):
                print("Variability: {:3.2f}s".format(timeLoss_variability))
    
        if config.getboolean('debug', 'lap_participant_pitstop') & self.is_pitting:
            print(emoji.emojize(":yellow_circle: {} has performed pit stop ({}s)").format(self.participant_id, simulated_pit_stop.service_time))
            
        #print(lap_time)

        # update race_time & race_lastLapTime
        self.race_time += lap_time
        self.race_lap += 1
        self.race_lastLapTime = lap_time


        # updating car wear
        self.update_wear(fuel_loss, tire_deg)


        # check if participant has to retire
        self.calc_retirement()


        return lap_time

    def update_wear(self, fuel_loss, tire_deg):
        
        if self.is_pitting:
            self.car_fuelMass = self.pit_refuelAmount * 15 # assuming 15 L for each lap
            self.car_tireDeg = 0
            self.stint_length = 1
        else:
            self.car_fuelMass += fuel_loss
            self.car_tireDeg += tire_deg
            self.stint_length += 1

        if self.car_tireDeg > 100:
            self.car_tireDeg = 100

        # removing is_pitting flag
        self.is_pitting = False
        self.pit_refuelAmount = 0
        

    
    def calc_retirement(self):
        has_to_retire = False
        retirement_reason = ""

        if self.car_fuelMass < 0:
            has_to_retire = True
            retirement_reason = "no more fuel"
        elif self.car_tireDAge > 99:
            has_to_retire = True
            retirement_reason = "no more tire"
        else:
            has_to_retire = False
        
        if has_to_retire:
            self.is_retired = True
            if config.getboolean('debug', 'lap_retirement'):
                print("!!! - {} has retired from the race! ({})".format(self.participant_id, retirement_reason))


    def calc_pitStopDecision(self):
        # calculating pit stop decision

        # check if selected race_strategy demands pit stop in this lap
        
        for planned_stop in self.race_strategy:
            if planned_stop["inlap"] == self.race_lap:
                #print(emoji.emojize(":red_circle: pitting!"))
                self.is_pitting = True
                self.pit_refuelAmount = planned_stop["refuel"]
        
"""