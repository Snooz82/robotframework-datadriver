# Copyright 2018-  René Rohner
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


"""
[
  {
    "test_case_name": "first",
    "arguments": {
      "${username}": "demo",
      "${password}": "mode"
    },
    "tags": [
      "tag1",
      "tag2",
      "smoke"
    ],
    "documentation": "This is the doc"
  },
  {
    "test_case_name": "second",
    "arguments": {
      "${username}": "${EMPTY}",
      "${password}": "mode"
    },
    "tags": [
      "tag1",
      "smoke"
    ],
    "documentation": "This is the doc"
  }
]
"""
from json import load
from .AbstractReaderClass import AbstractReaderClass
from .ReaderConfig import TestCaseData


class json_reader(AbstractReaderClass):
    def get_data_from_source(self):
        with open(self.file, 'r', encoding="utf-8") as json_file:
            return [TestCaseData(**test) for test in load(json_file)]
