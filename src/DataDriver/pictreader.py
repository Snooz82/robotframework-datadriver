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


import csv
import os


class PictReader:

    def __init__(self, file, testcase_table_name):
        self.file = file
        self.filename, self.file_extension = os.path.splitext(self.file)
        self.testcase_table_name = testcase_table_name
        self.data_table = None

    def get_data_from_pict(self):
        self._register_dialect()
        self._create_gemerated_file_from_model_file()
        self._read_generated_file_to_dictionaries()
        return self.data_table

    def _register_dialect(self):
        csv.register_dialect('PICT',
                             delimiter='\t',
                             skipinitialspace=False,
                             lineterminator='\r\n',
                             quoting=csv.QUOTE_NONE)

    def _create_gemerated_file_from_model_file(self):
        os.system(f'pict "{self.file}" > "{self.filename}.pictout"')

    def _read_generated_file_to_dictionaries(self):
        with open(f'{self.filename}.pictout', 'r', encoding='utf_8') as csvfile:
            reader = csv.reader(csvfile, 'PICT')
            table = {}
            header = []
            test_case_column = []
            for row_index, row in enumerate(reader):
                if row_index == 0:
                    header = row
                    for header_cell in header:
                        table[f'${{{header_cell}}}'] = []
                else:
                    for cell_index, cell in enumerate(row):
                        table[f'${{{header[cell_index]}}}'].append(cell)
                    test_case_column.append('')
            table[self.testcase_table_name] = test_case_column
        self.data_table = table
