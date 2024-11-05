import argparse
from emulator import environment


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--human", action="store_true", help="Enable human control mode."
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    environment.run(args.human)


if __name__ == "__main__":
    main()
