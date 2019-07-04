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
from .AbstractReaderClass import AbstractReaderClass


class xls_Reader(AbstractReaderClass):

    def get_data_from_source(self):
        data_frame = pd.read_excel(self.file, sheet_name=self.sheet_name, dtype=str).replace(np.nan, '', regex=True)
        self._analyse_header(list(data_frame))
        for row in data_frame.values.tolist():
            self._read_data_from_table(row)
        return self.data_table
