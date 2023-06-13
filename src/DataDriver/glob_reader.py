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


from glob import glob
from pathlib import Path

from DataDriver.AbstractReaderClass import AbstractReaderClass


class glob_reader(AbstractReaderClass):
    def get_data_from_source(self):
        self._read_glob_to_data_table()
        return self.data_table

    def _read_glob_to_data_table(self):
        self._analyse_header(["*** Test Cases ***", self.kwargs.get("arg_name", "${file_name}")])
        for match_path in sorted(glob(self.file)):
            path = Path(match_path).resolve()
            path_as_posix = path.as_posix()
            if path.is_file():
                test_case_name = path.stem
            elif path.is_dir():
                test_case_name = path.name
            else:
                test_case_name = str(path_as_posix)
            self._read_data_from_table([test_case_name, str(path_as_posix)])
