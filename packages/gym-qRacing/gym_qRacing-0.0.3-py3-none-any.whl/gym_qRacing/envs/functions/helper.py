from rich import print

class Helper:

    #
    # * this function performs all logging
    #
    @staticmethod
    def global_logging(config_logging, log_domain, log_msg):
        
        # only display log message, if the respective domain has been enabled in the config
        if config_logging[log_domain]:
            print(log_msg)

        return None

"""
    @staticmethod
    def format_pitStop_string(self, pitStops):
        # only print details for less than 5 stops

        if len(pitStops) < 6:
            string = str(len(pitStops)) + " -> ("

            for pitStop in pitStops:
                string += "" + str(pitStop.race_lap) + "/" + str(pitStop.refuel_amount) + " + "

            string += ")"
        else:
            string = str(len(pitStops))

        return string
"""