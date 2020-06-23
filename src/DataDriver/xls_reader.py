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
    import xlrd
    import numpy as np
except ImportError:
    raise ImportError("""Requirements (xlrd, numpy) for XLS support are not installed.
    Use 'pip install -U robotframework-datadriver[XLS]' to install XLS support.""")

from .AbstractReaderClass import AbstractReaderClass


class xls_reader(AbstractReaderClass):

    def get_data_from_source(self):
        work_book = xlrd.open_workbook(self.file)
        work_sheet = work_book.sheet_by_name(self.sheet_name)
        num_rows = work_sheet.nrows
        num_cols = work_sheet.ncols
        headers = []
        for i in range(num_cols):
            headers.append(work_sheet.cell(0, i).value)
        self._analyse_header(headers)

        row_values = []
        for i in range(1, num_rows):
            row = []
            for j in range(num_cols):
                row.append(work_sheet.cell(i, j).value)
            row_values.append(row)

        for row in row_values:
            self._read_data_from_table(row)
        return self.data_table
