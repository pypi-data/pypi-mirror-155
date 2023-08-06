import os
import warnings
from wukong.cli import cli_parser
import argcomplete


def main():
    parser = cli_parser.get_parser()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
