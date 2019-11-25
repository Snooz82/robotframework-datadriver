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
from DataDriver.AbstractReaderClass import AbstractReaderClass


class csv_reader(AbstractReaderClass):

    def get_data_from_source(self):
        self._register_dialects()
        self._read_file_to_data_table()
        return self.data_table

    def _register_dialects(self):
        if self.csv_dialect.lower() == 'userdefined':
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

    def _read_file_to_data_table(self):
        with open(self.file, 'r', encoding=self.csv_encoding) as csvfile:
            reader = csv.reader(csvfile, self.csv_dialect)
            for row_index, row in enumerate(reader):
                if row_index == 0:
                    self._analyse_header(row)
                else:
                    self._read_data_from_table(row)
