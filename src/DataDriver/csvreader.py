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


class CsvReader:

    def __init__(self,
                 file,
                 encoding,
                 testcase_table_name,
                 dialect='Excel-EU',
                 delimiter=';',
                 quotechar='"',
                 escapechar='\\',
                 doublequote=True,
                 skipinitialspace=False,
                 lineterminator='\r\n'
                 ):

        self.file = file
        self.csv_encoding = encoding
        self.csv_dialect = dialect
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.escapechar = escapechar
        self.doublequote = doublequote
        self.skipinitialspace = skipinitialspace
        self.lineterminator = lineterminator

        self.TESTCASE_TABLE_NAME = testcase_table_name
        self.data_table = None
        self.index = None

    def get_data_from_csv(self):
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
            table = {}
            header = []
            for row_index, row in enumerate(reader):
                if row_index == 0:
                    header = row
                    if header[0] == self.TESTCASE_TABLE_NAME:
                        for cell in header:
                            table[cell] = []
                    else:
                        raise SyntaxError('First column is not "'
                                          + self.TESTCASE_TABLE_NAME
                                          + '". This Column is mandatory.')
                else:
                    for cell_index, cell in enumerate(row):
                        table[header[cell_index]].append(cell)
            self.data_table = table
