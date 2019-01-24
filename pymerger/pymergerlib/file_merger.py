# Copyright (c) Alex-Christian Lazau
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""File merger class"""

from yapf.yapflib.yapf_api import FormatCode
from pymerger.pymergerlib.errors import PyMergerError
from pathlib import Path


class FileMerger():
    def __init__(self, args):
        self.files = []
        self.recursive = args.recursive
        self.debug = args.debug
        self.readFiles(args.paths, args.ignore)

        self.name = args.name
        self.no_format = args.no_format
        self.imports = {}

    def merge(self):
        out_string = ""

        with open(self.name, "w") as out_file:
            for file in self.files:
                with open(file, "r") as in_file:
                    in_file_string = in_file.read()
                    if in_file_string != "":
                        out_string += "\n"
                        out_string += self.extractImports(in_file_string)
                        out_string += "\n"

            if self.debug:
                print("\nBefore dropping local imports:\n{}\n".format(
                    self.imports))
            self.dropLocalImports()

            if self.debug:
                print("\nAfter dropping local imports:\n{}\n".format(
                    self.imports))

            imports_string = self.writeImports()
            if not imports_string:
                out_string = out_string.lstrip()
            elif out_string[:1] == "\n":
                out_string = out_string[1:]
            out_string = imports_string + out_string

            if not self.no_format:
                out_string, _ = FormatCode(out_string)
            out_file.write(out_string)

    def extractImports(self, file_content):
        lines = file_content.splitlines()
        delete_lines = []

        for i, line in enumerate(lines):
            if len(line) > 7:
                words = list(
                    filter(None, map(lambda x: x.strip(','), line.split())))

                if words[0] == "import":
                    if words[1] not in self.imports:
                        self.imports[words[1]] = {}
                        self.imports[words[1]]["as"] = set()
                    if 'as' in words:
                        self.imports[words[1]]["as"].add(words[3])
                    else:
                        self.imports[words[1]]["as"].add(words[1])
                    delete_lines.append(i)

                if words[0] == "from":
                    if words[1] not in self.imports:
                        self.imports[words[1]] = {}
                    if 'as' in words:
                        if words[3] not in self.imports[words[1]]:
                            self.imports[words[1]][words[3]] = set()
                        self.imports[words[1]][words[3]].add(words[5])
                    else:
                        for word in words[3:]:
                            if word not in self.imports[words[1]]:
                                self.imports[words[1]][word] = set()
                            self.imports[words[1]][word].add(word)
                    delete_lines.append(i)

        for i in sorted(delete_lines, reverse=True):
            del lines[i]

        return "\n".join(lines)

    def dropLocalImports(self):
        delete_key = []

        for local_import in self.imports:
            for file_name in self.files:
                if local_import == file_name[:-3].replace('/', '.'):
                    delete_key.append(local_import)

        for key in delete_key:
            del self.imports[key]

    def writeImports(self):
        out_string = ""

        for module, sub_modules in self.imports.items():
            for k, v in sub_modules.items():
                v = list(v)
                if k == "as":
                    pre_string = "import " + module
                    if v[0] == module:
                        out_string += pre_string + "\n"
                    else:
                        out_string += pre_string + " as " + v[0] + "\n"
                else:
                    pre_string = "from " + module + " import " + k
                    if k == v[0]:
                        out_string += pre_string + "\n"
                    else:
                        out_string += pre_string + " as " + v[0] + "\n"

        return out_string

    def readFiles(self, merge_paths, ignore_paths):
        ignore_paths = self.checkPaths(ignore_paths)
        for path in ignore_paths[:]:
            if Path(path).is_dir():
                ignore_paths += list(Path(path).glob('*.py'))
            else:
                ignore_paths.append(path)

        paths = self.checkPaths(merge_paths)
        for path in paths:
            if Path(path).is_dir():
                if self.recursive:
                    glob_paths = list(Path(path).rglob('*.py'))
                else:
                    glob_paths = list(Path(path).glob('*.py'))
                for glob_path in glob_paths:
                    if glob_path not in ignore_paths:
                        self.files.append("/".join(glob_path.parts))
            else:
                if path not in ignore_paths:
                    self.files.append(path)

        if self.debug:
            print("\nList of files to merge:\n{}\n".format(self.files))

    def checkPaths(self, paths):
        if not paths:
            return []

        if len(paths) == 1 and paths[0][-4:] == ".txt":
            with open(paths[0], "r") as paths:
                paths = list(filter(None, [line.rstrip() for line in paths]))

        for path in paths:
            if not Path(path).exists():
                raise PyMergerError(
                    "{}: File or directory path does not exist.".format(path))
            if Path(path).is_file() and path[-3:] != ".py":
                raise PyMergerError(
                    "{}: Wrong file type. Use a py file instead.".format(path))

        return paths
