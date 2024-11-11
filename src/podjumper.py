import argparse
from secrets import Secrets

def create_parser():
    parser = argparse.ArgumentParser(description="Command-line Todo List App")
    parser.add_argument("-s", "--secrets", metavar="", help="Generates secrets to then use in deployment")
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.secrets:
        print("asd")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()