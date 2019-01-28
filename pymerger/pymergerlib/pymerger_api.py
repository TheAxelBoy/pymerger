# Copyright (c) Alex-Christian Lazau
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""Entry point for PyMerger"""

from argparse import Namespace
from pymerger.pymergerlib.file_merger import FileMerger


def merge_with_config(config):
    merger = FileMerger(config)
    merger.merge()


def merge_files(paths,
                name="merged.py",
                no_format=False,
                recursive=False,
                debug=False,
                ignore=None):
    args = Namespace(
        paths=paths,
        name=name,
        no_format=no_format,
        recursive=recursive,
        debug=debug,
        ignore=ignore)
    merge_with_config(args)
