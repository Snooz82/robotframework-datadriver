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

from DataDriver.AbstractReaderClass import (
    AbstractReaderClass,
)
from DataDriver.ReaderConfig import (
    TestCaseData,
)

from pathlib import Path
import json


class generic_json_reader(AbstractReaderClass):
    """
    Generate TestCaseData from any JSON file.

    Useful when working on normalized structured data provided by APIs.

    Requires JSON file to be a list.
    """

    def get_data_from_source(
        self,
    ) -> list[TestCaseData]:
        file_path = Path(self.file)
        with file_path.open(encoding=self.csv_encoding) as json_file:
            json_data = json.load(json_file)

        if not isinstance(json_data, list):
            raise TypeError(f"Cannot generate test data. Data in {file_path} is not a list.")

        return [
            TestCaseData(arguments={f"${{{k}}}": v for k, v in data.items()}) for data in json_data
        ]
