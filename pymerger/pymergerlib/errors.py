# Copyright (c) Alex-Christian Lazau
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""PyMerger error object."""


class PyMergerError(Exception):
    """Error class for command line errors
       which result in clean errors without
       backtraces
    """
    pass
