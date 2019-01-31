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


import os.path
import csv
from copy import deepcopy

class DataDriver:
    ROBOT_LISTENER_API_VERSION = 3
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    TESTCASE_HEADER = '*** Test Cases ***'
    TAGS_HEADER = '[Tags]'
    DOC_HEADER = '[Documentation]'

    def __init__(self,
                 file=None,
                 dialect='Excel-DE',
                 encoding='cp1252'):

        self.ROBOT_LIBRARY_LISTENER = self

        self.file = file
        self.csv_dialect = dialect
        self.csv_encoding = encoding
        self.suite_source = None
        self.template_test = None
        self.template_keyword = None
        self.data_table = None


    def start_suite(self, suite, result):
        self.suite_source = suite.source
        self._create_data_table()
        self.template_test = suite.tests[0]
        self.template_keyword = self._get_template_keyword(suite)
        temp_test_list = list()
        for self.index, lines in enumerate(self.data_table[self.TESTCASE_HEADER]):
            self.test = None
            self._create_test_from_template()
            temp_test_list.append(self.test)
        suite.tests = temp_test_list

    def _create_data_table(self):
        if not self.file:
            self._get_data_file_from_suite_source()
        else:
            self._check_if_file_exists_as_path_or_in_suite()

        with open(self.file, 'r', encoding=self.csv_encoding) as csvfile:

            csv.register_dialect('Excel-DE',
                                 delimiter=';',
                                 quotechar='"',
                                 escapechar='\\',
                                 doublequote=True,
                                 skipinitialspace=False,
                                 lineterminator='\r\n',
                                 quoting=csv.QUOTE_ALL)

            reader = csv.reader(csvfile, self.csv_dialect)
            table = {}
            for row_index, row in enumerate(reader):
                if row_index == 0:
                    header = row
                    for cell in header:
                        table[cell] = []
                else:
                    for cell_index, cell in enumerate(row):
                        table[header[cell_index]].append(cell)

        self.data_table = table

    def _get_data_file_from_suite_source(self):
        suite_path_as_csv = str(self.suite_source[:self.suite_source.rfind('.')]) + '.csv'
        if os.path.isfile(suite_path_as_csv):
            self.file = suite_path_as_csv
        else:
            raise FileNotFoundError(
                'File attribute was empty. Tried to find '
                + suite_path_as_csv + ' but file does not exist.')

    def _check_if_file_exists_as_path_or_in_suite(self):
        if not os.path.isfile(self.file):
            suite_dir = str(os.path.dirname(self.suite_source))
            file_in_suite_dir = os.path.join(suite_dir, self.file)
            if os.path.isfile(file_in_suite_dir):
                self.file = file_in_suite_dir
            else:
                raise FileNotFoundError(
                    'File attribute was not a full path. Tried to find '
                    + file_in_suite_dir + ' but file does not exist.')

    def _get_template_keyword(self, suite):
        template = self.template_test.template
        if template:
            for keyword in suite.resource.keywords:
                if self._is_same_keyword(keyword.name, template):
                    return keyword
        raise AttributeError('Not "Test Template" found for first test case.')

    def _get_normalized_keyword(self, keyword):
        return keyword.lower().replace(' ', '').replace('_', '')

    def _is_same_keyword(self, first, second):
        return self._get_normalized_keyword(first) == self._get_normalized_keyword(second)


    def _create_test_from_template(self):
        self.test = deepcopy(self.template_test)
        self._replace_test_case_name()
        self._replace_test_case_keywords()
        self._add_test_case_tags()
        self._replace_test_case_doc()

    def _add_test_case_tags(self):
        if self.TAGS_HEADER in self.data_table:
            for tag in self.data_table[self.TAGS_HEADER][self.index].split(','):
                self.test.tags.add(tag.strip())

    def _replace_test_case_doc(self):
        if self.DOC_HEADER in self.data_table:
            self.test.doc = self.data_table[self.DOC_HEADER][self.index]

    def _replace_test_case_keywords(self):
        self.test.keywords.clear()
        if self.template_test.keywords.setup != None:
            self.test.keywords.create(name=self.template_test.keywords.setup.name, type='setup',
                                 args=self.template_test.keywords.setup.args)
        self.test.keywords.create(name=self.template_keyword.name,
                             args=self._get_template_args_for_index())
        if self.template_test.keywords.teardown != None:
            self.test.keywords.create(name=self.template_test.keywords.teardown.name, type='teardown',
                                 args=self.template_test.keywords.teardown.args)

    def _replace_test_case_name(self):
        if self.data_table[self.TESTCASE_HEADER][self.index] == '':
            for key in self.data_table.keys():
                if key[:1] == '$':
                    self.test.name = self.test.name.replace(key, self.data_table[key][self.index])
        else:
           self.test.name = self.data_table[self.TESTCASE_HEADER][self.index]

    def _get_template_args_for_index(self):
        return_args = []
        for arg in self.template_keyword.args:
            if arg in self.data_table:
                return_args.append(self.data_table[arg][self.index])
            else:
                return_args.append(arg)
        return return_args
