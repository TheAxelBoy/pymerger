PyMerger
========

PyMerger merges multiple python source files into one
source file and resolves simple local imports.

Example
-------

This simple example merges main.py and the python files
in the sub_folder directory and creates a merged file
named simple_merge.py. The output is formatted by
`YAPF <https://github.com/google/yapf>`_.

.. code-block:: shell

    pymerger -p main.py sub_folder -n simple_merge.py

Links
-----

* Code: https://github.com/TheAxelBoy/pymerger
* License: `MIT <https://github.com/TheAxelBoy/pymerger/blob/master/LICENSE>`_