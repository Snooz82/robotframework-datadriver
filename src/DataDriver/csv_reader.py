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
from .Abstract_Reader_Class import Abstract_Reader_Class
from .ReaderConfig import TestCaseData


class csv_Reader(Abstract_Reader_Class):

    def get_data_from_source(self):
        self._register_dialects()
        self._read_file_to_dictionaries()
        return self.data_table

    def _register_dialects(self):
        if self.csv_dialect == 'UserDefined':
            csv.register_dialect(self.csv_dialect,
                                 delimiter=self.delimiter,
                                 quotechar=self.quotechar,
                                 escapechar=self.escapechar,
                                 doublequote=self.doublequote,
                                 skipinitialspace=self.skipinitialspace,
                                 lineterminator=self.lineterminator,
                                 quoting=csv.QUOTE_ALL)
        elif self.csv_dialect == 'Excel-EU':
            csv.register_dialect(self.csv_dialect,
                                 delimiter=';',
                                 quotechar='"',
                                 escapechar='\\',
                                 doublequote=True,
                                 skipinitialspace=False,
                                 lineterminator='\r\n',
                                 quoting=csv.QUOTE_ALL)

    def _read_file_to_dictionaries(self):
        with open(self.file, 'r', encoding=self.csv_encoding) as csvfile:
            reader = csv.reader(csvfile, self.csv_dialect)
            self.test_case_column_id = None
            self.arguments_column_ids = []
            self.tags_column_id = None
            self.documentation_column_id = None
            self.header = []
            for row_index, row in enumerate(reader):
                if row_index == 0:
                    self._analyse_header(row)
                else:
                    self._read_data_from_table(row)

    def _analyse_header(self, row):
        self.header = row
        for cell_index, cell in enumerate(self.header):
            if cell_index == 0:
                if self._is_test_case_header(cell):
                    self.test_case_column_id = cell_index
                else:
                    raise SyntaxError(f'First column is not "{self.TESTCASE_TABLE_NAME}".'
                                      f' This Column is mandatory. it is {cell}')
            if self._is_variable(cell):
                self.arguments_column_ids.append(cell_index)
            elif self._is_tags(cell):
                self.tags_column_id = cell_index
            elif self._is_documentation(cell):
                self.documentation_column_id = cell_index

    def _read_data_from_table(self, row):

        test_case_name = row[self.test_case_column_id]

        arguments = {}
        for arguments_column_id in self.arguments_column_ids:
            arguments[self.header[arguments_column_id]] = row[arguments_column_id]

        tags = row[self.tags_column_id].split(',')

        documentation = row[self.documentation_column_id]

        self.data_table.append(TestCaseData(test_case_name, arguments, tags, documentation))
