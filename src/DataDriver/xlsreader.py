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

import pandas as pd
import numpy as np


class XlsReader:

    def __init__(self, file, sheet_name):
        self.file = file
        self.sheet_name = sheet_name

    def get_data_from_xls(self):
        data_frame = pd.read_excel(self.file, sheet_name=self.sheet_name, dtype=str).replace(np.nan, '', regex=True)
        table = {}
        for header in data_frame.columns:
            table[header] = data_frame[header].tolist()
        return table
