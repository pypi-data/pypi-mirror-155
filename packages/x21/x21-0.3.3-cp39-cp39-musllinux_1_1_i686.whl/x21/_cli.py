import argparse
from sys import version_info

from .__about__ import __version__
from ._encrypt_path import encrypt_paths


def cli(argv=None):
    parser = argparse.ArgumentParser(
        description=("x21 build tools."),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=get_version_text(),
        help="display version information",
    )

    subparsers = parser.add_subparsers(title="subcommands", required=True)

    parser_encrypt_paths = subparsers.add_parser(
        "encrypt",
        help="Encrypt Python code in files",
        aliases=["e"],
    )
    parser_encrypt_paths.add_argument(
        "input_files",
        type=str,
        nargs="+",
        help="Python files/directories to encrypt",
    )
    parser_encrypt_paths.set_defaults(
        func=lambda args: encrypt_paths(args.input_files, verbose=True)
    )

    args = parser.parse_args(argv)
    return args.func(args)


def get_version_text():
    python_version = f"{version_info.major}.{version_info.minor}.{version_info.micro}"
    version_text = "\n".join(
        [
            f"x21 {__version__} [Python {python_version}]",
            "Copyright (c) 2022 Nico Schlömer <nico.schloemer@gmail.com>",
        ]
    )
    return version_text
