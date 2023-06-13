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
try:
    from math import nan  # type: ignore

    import openpyxl  # type: ignore  # noqa: F401
    import pandas as pd  # type: ignore
except ImportError as err:
    raise ImportError(
        """Requirements (pandas, openpyxl) for XLSX support are not installed.
    Use 'pip install -U robotframework-datadriver[XLS]' to install XLSX support."""
    ) from err
from robot.utils import is_truthy  # type: ignore

from .AbstractReaderClass import AbstractReaderClass


class xlsx_reader(AbstractReaderClass):
    def get_data_from_source(self):
        dtype = object if is_truthy(getattr(self, "preserve_xls_types", False)) else str
        data_frame = self.read_data_frame_from_file(dtype)
        self._analyse_header(list(data_frame))
        for row_index, row in enumerate(data_frame.values.tolist()):
            try:
                self._read_data_from_table(row)
            except Exception as e:
                e.row = row_index + 1
                raise e
        return self.data_table

    def read_data_frame_from_file(self, dtype):
        return pd.read_excel(
            self.file, sheet_name=self.sheet_name, dtype=dtype, engine="openpyxl", na_filter=False
        ).replace(nan, "", regex=True)
