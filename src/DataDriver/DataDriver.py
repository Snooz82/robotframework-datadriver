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

__version__ = '0.0.4'


class DataDriver:
    """
           DataDriver is a Data-Driven Testing library for Robot Framework.

           This document explains how to use the DataDriver library listener.
           For information about installation, support, and more, please visit the
           [https://github.com/Snooz82/robotframework-datadriver|project pages].
           For more information about Robot Framework, see http://robotframework.org.

           DataDriver is used/imported as Library but does not provide keywords which can be used in a test.
           DataDriver uses the Listener Interface Version 3 to manipulate the test cases and creates new test cases based
           on a CSV-File that contains the data für Data-Driven Testing.

           == Table of contents ==

           - `What DataDriver does`
           - `How DataDriver works`
           - `Usage`
           - `Structure of test suite`
           - `Structure of data file`

           = What DataDriver does =

           DataDriver is an alternative approach to create Data-Driven Tests with Robot Framework.
           DataDriver creates multiple test cases based on a test template and data content of a CSV file.
           All created tests share the same test sequence (keywords) and differ in the test data.
           Because these tests are created on runtime only the template has to be specified within the robot test
           specification and the used data are specified in an external CSV file.


           = How DataDriver works =

           When the Data Driver is used in a test suite it will be activated before the test suite starts.
           It uses the Listener Interface Version 3 of Robot Framework to read and modify the test specification objects.
           After activation it searches for the ``Test Template`` -Keyword to analyze the ``[Arguments]`` is has.
           As a second step, it loads the data from the specified CSV file.
           Based on the ``Test Template`` -Keyword, Data Driver creates as much test cases as lines are in the CSV file.
           As values for the arguments of the ``Test Template`` -Keyword it reads values from the column of the CSV file
           with the matching name of the ``[Arguments]``.
           For each line of the CSV data table, one test case will be created.
           It is also possible to specify test case names, tags, and documentation for each test case in the specific
           test suite related CSV file.

           = Usage =

           Data Driver is a "Listener" but should not be set as a global listener as command line option of robot.
           Because Data Driver is a listener and a library at the same time it sets itself as a listener when this library
           is imported into a test suite.

           == Limitation ==

           === Eclipse plug-in RED ===
           There are known issues if the Eclipse plug-in RED is used. Because the debugging Listener of this tool
           pre-calculates the number of test cases before the creation of test cases by the Data Driver. This leads to the
           situation that the RED listener throws exceptions because it is called for each test step but the RED GUI
           already stopped debugging so that the listener cannot send Information to the GUI.
           This does not influence the execution in any way but produces a lot of unwanted exceptions in the Log.

           === Variable types ===
           In this early Version of DataDriver only scalar variables are supported.
           Lists and dictionaries may be added in the next releases.

           === No RPA support ===
           In this early Version, the design is made for test cases. RPA support may be added later if requested.

            == How to activate the Data Driver ==

           To activate the DataDriver for a test suite (one specific *.robot file) just import it as a library.
           You may also specify some options if the default parameters do not fit your needs.

           Example:
           | ***** *Settings* *****
           | *Library*          DataDriver
           | *Test Template*    Invalid Logins
           |

           = Structure of test suite =

           == Requirements ==
           In the Moment there are some requirements how a test suite must be structured so that the Data Driver can
           get all the information it needs.

           - only the first test case will be used as a template. All other test cases will be deleted.
           - Test cases have to be defined with a ``*Test Template*``. Reason for this is, that the DataDriver needs to know the names of the test case arguments. Test cases do not have named arguments. Keywords do.
           - The keyword which is used as ``*Test Template*`` must be defined within the test suite (in the same \*.robot file). If the keyword which is used as ``Test Template`` is defined in a ``Resource`` the Data Driver has no access to its arguments names.

           == Example Test Suite ==

           | ***** *Settings* *****
           | *Library*           DataDriver
           | *Resource*          login_resources.robot
           | *Suite Setup*       Open my Browser
           | *Suite Teardown*    Close Browsers
           | *Test Setup*        Open Login Page
           | *Test Template*     Invalid Login
           |
           | ***** *Test Cases* *****
           | Login with user _'${username}'_ and password _'${password}'_    Default    UserData
           |
           | ***** *Keywords* *****
           | Invalid login
           |     *[Arguments]*    _${username}_    _${password}_
           |     Input username    _${username}_
           |     Input pwd    _${password}_
           |     click login button
           |     Error page should be visible

           In this example, the Data Driver is activated by using it as a Library. It is used with default settings.

           As ``Test Template`` the keyword ``Invalid Login`` is used. This keyword has two arguments.
           Argument names are _${username}_ and _${password}_. These names have to be in the CSV file as column header.
           The test case has two variable names included in its name, which does not have any functionality in
           Robot Framework. However, the Data Driver will use the test case name as a template name and replaces the
           variables with the specific value of the single generated test case.

           This template test will only be used as a template. The specified data ``Default`` and ``UserData`` would only
           be used, if no CSV file has been found.

           = Structure of data file =

           == min. required columns ==

           - ***** *Test Cases* ***** column has to be the first one.
           - *Argument columns*: For each argument of the ``Test Template`` keyword one column must be existing in the CSV file as data source. The name of this column must match the variable name and syntax.

           == optional columns ==

           - *[Tags]* column may be used to add specifically to a test case. Tags may be comma separated.
           - *[Documentation]* column may be used to add specific test case documentation.

           == Example CSV file ==

           | = ***** Test Cases ***** = | = ${username} = | = ${password} = | = [Tags] = | = [Documentation] =                                         |
           | Right user empty pass      | demo            | ${EMPTY}        | 1          | This is a test case documentation of the first one.         |
           | Right user wrong pass      | demo            | FooBar          | 2          |                                                             |
           | empty user mode pass       | ${EMPTY}        | mode            | 1,2,3,4    | This test case has the Tags 1,2,3 and 4 assigned.           |
           |                            | ${EMPTY}        | ${EMPTY}        |            | This test case has a generated name based on template name. |
           |                            | ${EMPTY}        | FooBar          |            | This test case has a generated name based on template name. |
           |                            | FooBar          | mode            |            | This test case has a generated name based on template name. |
           |                            | FooBar          | ${EMPTY}        |            | This test case has a generated name based on template name. |
           |                            | FooBar          | FooBar          |            | This test case has a generated name based on template name. |

           In this CSV file, eight test cases are defined. Each line specifies one test case.
           The first two test cases have specific names. The other six test cases will generate names based on
           template test cases name with the replacement of variables in this name.
           The order of columns is irrelevant except the first column, ``*** Test Cases ***``

           == Encoding and CSV Dialect ==
           CSV is far away from well designed and has absolutely no "common" format.
           Therefore it is possible to define your own dialect or use predefined.
           The default is Excel-EU which is a semicolon separated file.

           These Settings are changeable as options of the Data Driver Library.

           === file= ===
           - None(default): Data Driver will search in the test suites folder if a *.csv file with the same name than the test suite *.robot exists
           - absolute Path: If not None, Data Driver tries to find the given CSV file as an absolute path.
           - relative Path: If the option does not point to a CSV file as an absolute path, Data Driver tries to find a CSV file relative to the folder where the test suite is located.

           === encoding= ===
           may set the encoding of the CSV file.
           i.e. cp1252, ascii, iso-8859-1, latin-1, utf_8, utf_16, utf_16_be, utf_16_le, etc...
           https://docs.python.org/3.7/library/codecs.html#standard-encodings

           === dialect= ===
           You may change the CSV Dialect here.
           If the Dialect is set to 'UserDefined' the following options are used. Otherwise, they are ignored.

           supported Dialects are:

           | class excel(Dialect):
           |     """"Describe the usual properties of Excel-generated CSV files.""""
           |     delimiter = ','
           |     quotechar = '"'
           |     doublequote = True
           |     skipinitialspace = False
           |     lineterminator = '\\r\\n'
           |     quoting = QUOTE_MINIMAL
           | register_dialect("excel", excel)
           | 
           | class excel_tab(excel):
           |     """"Describe the usual properties of Excel-generated TAB-delimited files.""""
           |     delimiter = '\\t'
           | register_dialect("excel-tab", excel_tab)
           | 
           | class unix_dialect(Dialect):
           |     """"Describe the usual properties of Unix-generated CSV files.""""
           |     delimiter = ','
           |     quotechar = '"'
           |     doublequote = True
           |     skipinitialspace = False
           |     lineterminator = '\\n'
           |     quoting = QUOTE_ALL
           | register_dialect("unix", unix_dialect)


           Defaults:
           |    file=None,
           |    encoding='cp1252',
           |    dialect='Excel-EU',
           |    delimiter=';',
           |    quotechar='"',
           |    escapechar='\\',
           |    doublequote=True,
           |    skipinitialspace=False,
           |    lineterminator='\\r\\n'

       """
    ROBOT_LISTENER_API_VERSION = 3
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    TESTCASE_HEADER = '*** Test Cases ***'
    TAGS_HEADER = '[Tags]'
    DOC_HEADER = '[Documentation]'

    def __init__(self,
                 file=None,
                 encoding='cp1252',
                 dialect='Excel-EU',
                 delimiter=';',
                 quotechar='"',
                 escapechar='\\',
                 doublequote=True,
                 skipinitialspace=False,
                 lineterminator='\r\n'
                 ):
        """
        :param file:
        :param encoding:
        :param dialect:
        :param delimiter:
        :param quotechar:
        :param escapechar:
        :param doublequote:
        :param skipinitialspace:
        :param lineterminator:
        """
        self.ROBOT_LIBRARY_LISTENER = self

        self.file = file
        self.csv_encoding = encoding
        self.csv_dialect = dialect
        self.user_dialect = {'delimiter': delimiter,
                             'quotechar': quotechar,
                             'escapechar': escapechar,
                             'doublequote': doublequote,
                             'skipinitialspace': skipinitialspace,
                             'lineterminator': lineterminator
                             }

        self.suite_source = None
        self.template_test = None
        self.template_keyword = None
        self.data_table = None
        self.index = None

    # noinspection PyUnusedLocal
    def _start_suite(self, suite, result):
        """Called when a test suite starts.
        Data and result are model objects representing the executed test suite and its execution results, respectively.

        :param suite: class robot.running.model.TestSuite(name='', doc='', metadata=None, source=None)
        :param result: NOT USED
        """
        self.suite_source = suite.source
        self._create_data_table()
        self.template_test = suite.tests[0]
        self.template_keyword = self._get_template_keyword(suite)
        temp_test_list = list()
        for self.index, lines in enumerate(self.data_table[self.TESTCASE_HEADER]):
            # self.test = None
            self._create_test_from_template()
            temp_test_list.append(self.test)
        suite.tests = temp_test_list

    def _create_data_table(self):
        """
        this function creates a dictionary which contains all data from data file.
        Keys are header names.
        Values are data of this column as array.
        """
        if not self.file:
            self._get_data_file_from_suite_source()
        else:
            self._check_if_file_exists_as_path_or_in_suite()

        with open(self.file, 'r', encoding=self.csv_encoding) as csvfile:

            if self.csv_dialect == 'UserDefined':
                csv.register_dialect(self.csv_dialect,
                                     delimiter=self.user_dialect['delimiter'],
                                     quotechar=self.user_dialect['quotechar'],
                                     escapechar=self.user_dialect['escapechar'],
                                     doublequote=self.user_dialect['doublequote'],
                                     skipinitialspace=self.user_dialect['skipinitialspace'],
                                     lineterminator=self.user_dialect['lineterminator'],
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

            reader = csv.reader(csvfile, self.csv_dialect)
            table = {}
            header = []
            for row_index, row in enumerate(reader):
                if row_index == 0:
                    header = row
                    if header[0] == self.TESTCASE_HEADER:
                        for cell in header:
                            table[cell] = []
                    else:
                        raise SyntaxError('First column is not "'
                                          + self.TESTCASE_HEADER
                                          + '". This Column is mandatory.')
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
        raise AttributeError('No "Test Template" keyword found for first test case.')

    # noinspection PyMethodMayBeStatic
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
        if self.template_test.keywords.setup is not None:
            self.test.keywords.create(name=self.template_test.keywords.setup.name, type='setup',
                                      args=self.template_test.keywords.setup.args)
        self.test.keywords.create(name=self.template_keyword.name,
                                  args=self._get_template_args_for_index())
        if self.template_test.keywords.teardown is not None:
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
