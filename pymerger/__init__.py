# Copyright (c) Alex-Christian Lazau
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""PyMerger.

PyMerger merges multiple python source files into one
source file and resolves simple local imports.
"""

from argparse import ArgumentParser
import sys

from pymerger.pymergerlib.pymerger_api import Merge
from pymerger.pymergerlib.errors import PyMergerError

__version__ = '0.1.0'


def main(argv):
    """Main program."""
    parser = ArgumentParser()

    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        default=False,
        help="check recursively for py files "
        "in all directories. Only used for -p.")
    parser.add_argument(
        "-p",
        "--paths",
        nargs="+",
        metavar="PATH",
        required=True,
        help="use a list of paths or a txt file containing "
        "the paths for the files to merge. Using a "
        "directory will include all py files in that "
        "directory")
    parser.add_argument(
        "-n", "--name", default="merged.py", help="name of output file")
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        default=False,
        help="check recursively for py files "
        "in all directories. Only used for -p.")
    parser.add_argument(
        "--ignore",
        nargs="+",
        metavar="PATH",
        default=None,
        help="same use as -p, but instead ignores "
        "the specified files. This always "
        "has highest priority")
    parser.add_argument(
        "--no-format",
        action="store_true",
        default=False,
        help="do not use yapf to format the code")
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        default=False,
        help="use in case of debugging purposes "
        "for reporting bugs")

    args = parser.parse_args(argv[1:])

    if args.version:
        print('pymerger {}'.format(__version__))
        return 0

    Merge(args)
    return 0


def run_pymerger():
    try:
        sys.exit(main(sys.argv))
    except PyMergerError as e:
        sys.stderr.write('pymerger: ' + str(e) + '\n')
        sys.exit(1)


if __name__ == "__main__":
    run_pymerger()
