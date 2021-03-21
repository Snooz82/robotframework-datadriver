# Copyright 2021-  René Rohner
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This Reader has initialy been created by Samual Montgomery-Blinn (https://github.com/montsamu)
# Thanks for this contribution


from os.path import normpath, basename, splitext, abspath, isfile, isdir
from glob import glob

from DataDriver.AbstractReaderClass import AbstractReaderClass


class glob_reader(AbstractReaderClass):
    def get_data_from_source(self):
        self._read_glob_to_data_table()
        return self.data_table

    def _read_glob_to_data_table(self):
        self._analyse_header(["*** Test Cases ***", self.kwargs.get("arg_name", "${file_name}")])
        for match_path in sorted(glob(self.file)):
            match_path = abspath(match_path).replace("\\", "/")
            if isfile(match_path):
                test_case_name = basename(splitext(match_path)[0])
            elif isdir(match_path):
                test_case_name = basename(normpath(match_path))
            else:
                test_case_name = match_path
            self._read_data_from_table([test_case_name, match_path])
