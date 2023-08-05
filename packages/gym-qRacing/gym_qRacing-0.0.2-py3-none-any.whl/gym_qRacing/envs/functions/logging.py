from rich.console import Console
from rich.table import Table

class Logging:

    #
    # * this function displays a table detailing the timings of a simulated lap
    #
    @staticmethod
    def log_lap_timings(race_lap, race_grid):
        
        # * initialize table
        table = Table(title="Timings for Lap #{}".format(race_lap), show_header=True, header_style="bold magenta")
        table.add_column("Pos", style="dim")
        table.add_column("Name", width=8)
        table.add_column("Race Time", justify="right")
        table.add_column("Lap Time", justify="right")
        table.add_column("S1", justify="right")
        table.add_column("S2", justify="right")
        table.add_column("S3", justify="right")
        table.add_column("S4", justify="right")
        table.add_column("S5", justify="right")
        table.add_column("FuelMass", justify="right")
        table.add_column("TireDeg", justify="right")
        


        # * fill information into table
        # ? this should be done by iterating over the complete race_grid


        # iterating over all participants in race_grid
        for idx_participant, participant in enumerate(race_grid):
            wear_fuelCon = participant.log['laps'][race_lap]['wear_fuelCon']
            wear_tireDeg = participant.log['laps'][race_lap]['wear_tireDeg']

            # adding a row for each participant to the table
            table.add_row(
                str(participant.race_position),
                participant.participant_id,
                "{:10.2f}s".format(participant.race_time),
                "{:10.2f}s".format(participant.log['laps'][race_lap]['lap_time']),
                "{:10.2f}s".format(participant.log['laps'][race_lap]['sectors']['S1']['sector_time']),
                "{:10.2f}s".format(participant.log['laps'][race_lap]['sectors']['S2']['sector_time']),
                "{:10.2f}s".format(participant.log['laps'][race_lap]['sectors']['S3']['sector_time']),
                "{:10.2f}s".format(participant.log['laps'][race_lap]['sectors']['S4']['sector_time']),
                "{:10.2f}s".format(participant.log['laps'][race_lap]['sectors']['S5']['sector_time']),
                str(f'{participant.car_fuelMass:10.2f}l (-{wear_fuelCon:1.2f}l)'),
                str(f'{participant.car_tireDeg:10.2f}% (-{wear_tireDeg:1.2f}%)'),
            )





        # * display the table
        #print("\n")
        console = Console()
        console.print(table)
        print("\n")


    #
    # * this function displays a table detailing the generated starting grid
    #
    @staticmethod
    def log_starting_grid(race_lap, race_grid):
        
        # * initialize table
        table = Table(title="Generated starting grid", show_header=True, header_style="bold magenta")
        table.add_column("Pos", style="dim")
        table.add_column("Name", width=8)
        table.add_column("FuelMass", justify="right")
        table.add_column("TireDeg", justify="right")
        


        # * fill information into table
        # ? this should be done by iterating over the complete race_grid


        for idx_participant, participant in enumerate(race_grid):
            table.add_row(
                str(participant.race_position),
                participant.participant_id,
                str(f'{participant.car_fuelMass:10.2f}l'),
                str(f'{participant.car_tireDeg:10.2f}%'),
            )





        # * display the table
        #print("\n")
        console = Console()
        console.print(table)
        print("\n")



    #
    # * this function displays a table detailing the applyed models of a simulated lap
    #
    @staticmethod
    def log_lap_models(race_lap, race_grid):
        
        # TODO: display calculated fuelCon, tireDeg and respective time penalties
        return None