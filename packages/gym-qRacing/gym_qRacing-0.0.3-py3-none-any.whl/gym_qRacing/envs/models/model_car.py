from ..functions import Helper

class model_car():
    #
    # * this function calculates the fuel consumption
    #
    # TODO: implement calculation
    # ? could be expressed as linear function
    @staticmethod
    def calc_fuelConsumption(sector, participant):
        fuel_consumption = sector.wear_fuelCon

        return fuel_consumption


    #
    # * this function calculates the tire degradation
    #
    # TODO: implement calculation
    # ? could be expressed as logarithmic function
    @staticmethod
    def calc_tireDeg(sector, participant):
        tireDeg = sector.wear_tireDeg

        return tireDeg

    #
    # * this function calculates the time loss due to fuel mass
    #
    # TODO: implement real calculation model
    @staticmethod
    def calc_timeLoss_fuelMass(participant, sector):
        timeLoss_fuelMass = sector.timeLoss_fuelMass * participant.car_fuelMass

        return timeLoss_fuelMass


    #
    # * this function calculates the time loss due to tire degradation
    #
    # TODO: implement real calculation model
    @staticmethod
    def calc_timeLoss_tireDeg(participant, sector):
        timeLoss_tireDeg = sector.timeLoss_tireDeg * participant.car_tireDeg

        return timeLoss_tireDeg

