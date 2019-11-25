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
from .ReaderConfig import TestCaseData
import re


class AbstractReaderClass:

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
        self.kwargs = reader_config.kwargs

        self.test_case_column_id = None
        self.arguments_column_ids = []
        self.tags_column_id = None
        self.documentation_column_id = None
        self.header = []
        self.data_table = []

        self.TESTCASE_TABLE_NAME = ReaderConfig.TEST_CASE_TABLE_NAME
        self.TEST_CASE_TABLE_PATTERN = r'(?i)^(\*+\s*test ?cases?[\s*].*)'
        self.TASK_TABLE_PATTERN = r'(?i)^(\*+\s*tasks?[\s*].*)'
        self.VARIABLE_PATTERN = r'([$@&]{1}\{)(.*?)(\})'
        self.TAGS_PATTERN = r'(?i)(\[)(tags)(\])'
        self.DOCUMENTATION_PATTERN = r'(?i)(\[)(documentation)(\])'

    def get_data_from_source(self):
        raise NotImplementedError("This method should be implemented and return self.data_table to DataDriver...")

    def _is_test_case_header(self, header_string: str):
        is_test = re.fullmatch(self.TEST_CASE_TABLE_PATTERN, header_string)
        is_task = re.fullmatch(self.TASK_TABLE_PATTERN, header_string)
        if is_task or is_test:
            return True

    def _is_variable(self, header_string: str):
        if re.match(self.VARIABLE_PATTERN, header_string):
            return True

    def _is_tags(self, header_string: str):
        if re.match(self.TAGS_PATTERN, header_string):
            return True

    def _is_documentation(self, header_string: str):
        if re.match(self.DOCUMENTATION_PATTERN, header_string):
            return True

    def _analyse_header(self, header_cells):
        self.header = header_cells
        for cell_index, cell in enumerate(self.header):
            if self._is_test_case_header(cell):
                self.test_case_column_id = cell_index
            if self._is_variable(cell):
                self.arguments_column_ids.append(cell_index)
            elif self._is_tags(cell):
                self.tags_column_id = cell_index
            elif self._is_documentation(cell):
                self.documentation_column_id = cell_index

    def _read_data_from_table(self, row):
        test_case_name = row[self.test_case_column_id] if self.test_case_column_id is not None else ''
        arguments = {}
        for arguments_column_id in self.arguments_column_ids:
            arguments[self.header[arguments_column_id]] = row[arguments_column_id]
        tags = [t.strip() for t in row[self.tags_column_id].split(',')] if self.tags_column_id else None
        documentation = row[self.documentation_column_id] if self.documentation_column_id else ''

        self.data_table.append(TestCaseData(test_case_name, arguments, tags, documentation))
