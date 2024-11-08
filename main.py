import argparse
from emulator import environment

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run Pokemon Red."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--headless", action="store_true", help="Enable Headless Parallel Training Mode"
    )
    group.add_argument(
        "--human", action="store_true", help="Enable Human Control Mode."
    )
    group.add_argument(
        "--train", action="store_true", help="Run Graphical Training Mode"
    )
    group.add_argument(
        "--eval", action="store_true", help="Run Evaluation Mode"
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    environment.run(args)
