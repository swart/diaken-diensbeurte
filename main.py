import argparse
from scheduler import Scheduler, Strategy


def main():
    parser = argparse.ArgumentParser(
        description="Skep diaken diensbeurte in 'n lukrake en regverdige manier. Die inset is 'n lys diakens (diakens.txt) en die uitset is PDF en CSV lêers (./data/)."
    )
    parser.add_argument(
        "-m",
        "--maande",
        type=int,
        default=6,
        help="Hoeveelheid maande om die diensbeurte uit te werk. Verstekwaarde is 6.",
    )
    parser.add_argument(
        "-s",
        "--strategie",
        type=int,
        choices=[1, 2],
        default=1,
        help="Strategie vir indeling. 1: Shuffle en deel diakens in elke sondag. 2: Shuffle die hele diakenlys elke siklus.",
    )
    args = parser.parse_args()

    scheduler = Scheduler(months=args.maande, strategy=Strategy(args.strategie))
    scheduler.generate()


if __name__ == "__main__":
    main()
