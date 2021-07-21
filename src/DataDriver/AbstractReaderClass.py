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

from abc import ABC
from re import compile
from typing import List

from .ReaderConfig import ReaderConfig
from .ReaderConfig import TestCaseData
from .search import search_variable

from robot.libraries.BuiltIn import BuiltIn  # type: ignore
from robot.utils import DotDict  # type: ignore


built_in = BuiltIn()


class AbstractReaderClass(ABC):
    def __init__(self, reader_config: ReaderConfig):

        self.reader_config = reader_config
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
        self.list_separator = reader_config.list_separator
        self.kwargs = reader_config.kwargs
        for key, value in reader_config.kwargs.items():
            setattr(self, key, value)

        self.test_case_column_id = None
        self.arguments_column_ids: List = list()
        self.tags_column_id = None
        self.documentation_column_id = None
        self.header: List = list()
        self.data_table: List = list()

        self.TESTCASE_TABLE_NAME = ReaderConfig.TEST_CASE_TABLE_NAME
        self.TEST_CASE_TABLE_PATTERN = compile(r"(?i)^(\*+\s*test ?cases?[\s*].*)")
        self.TASK_TABLE_PATTERN = compile(r"(?i)^(\*+\s*tasks?[\s*].*)")
        self.VARIABLE_PATTERN = compile(r"([$@&e]\{)(.*?)(\})")
        self.TAGS_PATTERN = compile(r"(?i)(\[)(tags)(\])")
        self.DOCUMENTATION_PATTERN = compile(r"(?i)(\[)(documentation)(\])")
        self.LIT_EVAL_PATTERN = compile(r"e\{(.+)\}")

    def get_data_from_source(self):
        raise NotImplementedError(
            "This method should be implemented and return self.data_table to DataDriver..."
        )

    def _is_test_case_header(self, header_string: str):
        is_test = self.TEST_CASE_TABLE_PATTERN.fullmatch(header_string)
        is_task = self.TASK_TABLE_PATTERN.fullmatch(header_string)
        return is_task or is_test

    def _is_variable(self, header_string: str):
        return self.VARIABLE_PATTERN.match(header_string)

    def _is_tags(self, header_string: str):
        return self.TAGS_PATTERN.match(header_string)

    def _is_documentation(self, header_string: str):
        return self.DOCUMENTATION_PATTERN.match(header_string)

    def _analyse_header(self, header_cells):
        self.header = header_cells
        for cell_index, cell in enumerate(self.header):
            if self._is_test_case_header(cell):
                self.test_case_column_id = cell_index
            elif self._is_variable(cell):
                self.arguments_column_ids.append(cell_index)
            elif self._is_tags(cell):
                self.tags_column_id = cell_index
            elif self._is_documentation(cell):
                self.documentation_column_id = cell_index

    def _read_data_from_table(self, row):
        test_case_name = (
            row[self.test_case_column_id] if self.test_case_column_id is not None else ""
        )
        arguments = {}
        for arguments_column_id in self.arguments_column_ids:
            variable_string = self.header[arguments_column_id]
            variable_value = row[arguments_column_id]
            if self.LIT_EVAL_PATTERN.fullmatch(variable_string):
                variable_string = f"${variable_string[1:]}"
                variable_value = built_in.replace_variables(variable_value)
                variable_value = built_in.evaluate(variable_value)
            variable_match = search_variable(variable_string)
            if variable_match.is_variable:
                arguments.update(
                    self._get_arguments_entry(variable_match, variable_value, arguments)
                )
        tags = (
            [t.strip() for t in row[self.tags_column_id].split(",")]
            if self.tags_column_id
            else None
        )
        documentation = row[self.documentation_column_id] if self.documentation_column_id else ""

        self.data_table.append(TestCaseData(test_case_name, arguments, tags, documentation))

    def _get_arguments_entry(self, variable_match, variable_value, arguments):
        base = variable_match.base
        items = variable_match.items
        if variable_match.is_list_variable:
            if not variable_value:
                variable_value = []
            else:
                variable_value = [
                    built_in.replace_variables(var)
                    for var in (str(variable_value).split(self.list_separator))
                ]
        elif variable_match.is_dict_variable:
            variable_value = built_in.create_dictionary(
                *(str(variable_value).split(self.list_separator))
            )
        if "." in base:  # is dot notated advanced variable dictionary ${dict.key.subkey}
            base, *items = base.split(".")
            variable_value = self._update_argument_dict(arguments, base, items, variable_value)
        elif items:  # is dictionary syntax ${dict}[key][subkey]
            variable_value = self._update_argument_dict(arguments, base, items, variable_value)

        return {self._as_var(base): variable_value}

    def _update_argument_dict(self, arguments, base, items, value):
        if self._as_var(base) not in arguments:
            arguments[self._as_var(base)] = built_in.create_dictionary()
        argument = arguments[self._as_var(base)]

        if isinstance(argument, DotDict):
            selected_key = argument
            for key in items:
                if key != items[-1]:
                    if key not in selected_key or not isinstance(selected_key[key], DotDict):
                        selected_key[key] = built_in.create_dictionary()
                    selected_key = selected_key[key]
            selected_key[items[-1]] = built_in.replace_variables(value)
            return argument
        else:
            raise TypeError(f"{self._as_var(base)} is defined with a wrong type. Not defaultdict.")

    def _as_var(self, base):
        return f"${{{base}}}"
