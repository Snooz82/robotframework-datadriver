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


from .ReaderConfig import ReaderConfig


class Abstract_Reader_Class:

    def __init__(self, reader_config: ReaderConfig):

        self.file = reader_config.file
        self.csv_encoding = reader_config.encoding
        self.csv_dialect = reader_config.dialect
        self.delimiter = reader_config.delimiter
        self.quotechar = reader_config.quotechar
        self.escapechar = reader_config.escapechar
        self.doublequote = reader_config.doublequote
        self.skipinitialspace = reader_config.skipinitialspace
        self.lineterminator = reader_config.lineterminator
        self.sheet_name = reader_config.sheet_name
        self.TESTCASE_TABLE_NAME = reader_config.testcase_table_name

    def get_data_from_source(self):
        raise NotImplementedError("This method should be implemented and return the Data to DataDriver...")
