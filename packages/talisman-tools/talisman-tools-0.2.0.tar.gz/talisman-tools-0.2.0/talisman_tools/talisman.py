from argparse import ArgumentParser

from talisman_tools.commands import SUBPARSERS
from talisman_tools.parser_helper import configure_subparsers


def main():
    parser = ArgumentParser(description='Talisman tools')
    configure_subparsers(parser, SUBPARSERS)

    args = parser.parse_args()
    action = args.action()
    action(args)  # pass control to relevant subparser


if __name__ == "__main__":
    main()
