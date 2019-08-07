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

import os
import os.path
import re
from copy import deepcopy
from .ReaderConfig import ReaderConfig
from .ReaderConfig import TestCaseData
from robot.libraries.BuiltIn import BuiltIn
import importlib

__version__ = '0.3.0'


class DataDriver:
    """|
|

===================================================
robotframework-datadriver
===================================================

DataDriver is a Data-Driven Testing library for Robot Framework.
This document explains how to use the DataDriver library listener. For
information about installation, support, and more, please visit the
`project page <https://github.com/Snooz82/robotframework-datadriver>`_

For more information about Robot Framework, see http://robotframework.org.

DataDriver is used/imported as Library but does not provide keywords
which can be used in a test. DataDriver uses the Listener Interface
Version 3 to manipulate the test cases and creates new test cases based
on a Data-File that contains the data for Data-Driven Testing. These
data file may be .csv , .xls or .xlsx files.

Data Driver is also able to cooperate with Microsoft PICT. An Open
Source Windows tool for data combination testing. Pict is able to
generate data combinations based on textual model definitions.
https://github.com/Microsoft/pict

|

Installation
------------

If you already have Python >= 3.6 with pip installed, you can simply
run:

``pip install --upgrade robotframework-datadriver``

or if you have Python 2 and 3 installed in parallel you may use

``pip3 install --upgrade robotframework-datadriver``

|

Table of contents
-----------------

-  `What DataDriver does <#WhatDataDriverdoes>`__
-  `How DataDriver works <#HowDataDriverworks>`__
-  `Usage <#Usage>`__
-  `Structure of test suite <#Structureoftestsuite>`__
-  `Structure of data file <#Structureofdatafile>`__
-  `Data Sources <#DataSources>`__
-  `Encoding and CSV Dialect <#EncodingandCSVDialect>`__

|

What DataDriver does
--------------------

DataDriver is an alternative approach to create Data-Driven Tests with
Robot Framework. DataDriver creates multiple test cases based on a test
template and data content of a csv or Excel file. All created tests
share the same test sequence (keywords) and differ in the test data.
Because these tests are created on runtime only the template has to be
specified within the robot test specification and the used data are
specified in an external data file.

DataDriver gives an alternative to the build in data driven approach
like:

.. code :: robotframework

    *** Settings ***
    Resource    login_resources.robot

    Suite Setup    Open my Browser
    Suite Teardown    Close Browsers
    Test Setup      Open Login Page
    Test Template    Invalid login


    *** Test Cases ***       User        Passwort
    Right user empty pass    demo        ${EMPTY}
    Right user wrong pass    demo        FooBar

    Empty user right pass    ${EMPTY}    mode
    Empty user empty pass    ${EMPTY}    ${EMPTY}
    Empty user wrong pass    ${EMPTY}    FooBar

    Wrong user right pass    FooBar      mode
    Wrong user empty pass    FooBar      ${EMPTY}
    Wrong user wrong pass    FooBar      FooBar

    *** Keywords ***
    Invalid login
        [Arguments]    ${username}    ${password}
        Input username    ${username}
        Input pwd    ${password}
        click login button
        Error page should be visible

This inbuild approach is fine for a hand full of data and a hand full of
test cases. If you have generated or calculated data and specially if
you have a variable amount of test case / combinations these robot files
becom quite a pain. With datadriver you may write the same test case
syntax but only once and deliver the data from en external data file.

One of the rare reasons when Microsoft® Excel or LibreOffice Calc may be
used in testing… ;-)

`See example test suite <#example-suite>`__

`See example csv table <#example-csv>`__

|

How DataDriver works
--------------------

When the DataDriver is used in a test suite it will be activated before
the test suite starts. It uses the Listener Interface Version 3 of Robot
Framework to read and modify the test specification objects. After
activation it searches for the ``Test Template`` -Keyword to analyze the
``[Arguments]`` it has. As a second step, it loads the data from the
specified CSV file. Based on the ``Test Template`` -Keyword, DataDriver
creates as much test cases as lines are in the CSV file. As values for
the arguments of the ``Test Template`` -Keyword it reads values from the
column of the CSV file with the matching name of the ``[Arguments]``.
For each line of the CSV data table, one test case will be created. It
is also possible to specify test case names, tags and documentation for
each test case in the specific test suite related CSV file.

|

Usage
-----

Data Driver is a "Listener" but should not be set as a global listener
as command line option of robot. Because Data Driver is a listener and a
library at the same time it sets itself as a listener when this library
is imported into a test suite.

To use it, just use it as Library in your suite. You may use the first
argument (option) which may set the file name or path to the data file.

Without any options set, it loads a .csv file which has the same name
and path like the test suite .robot .


**Example:**

.. code :: robotframework

    *** Settings ***
    Library    DataDriver

Options
~~~~~~~

.. code :: robotframework

    *** Settings ***
    Library    DataDriver
    ...    file=None
    ...    encoding=cp1252
    ...    dialect=Excel-EU
    ...    delimiter=;
    ...    quotechar="
    ...    escapechar=\\\\
    ...    doublequote=True
    ...    skipinitialspace=False
    ...    lineterminator=\\r\\n
    ...    sheet_name=0


|

Encoding
^^^^^^^^

``encoding`` must be set if it shall not be cp1252

**cp1252** is the same like:

- Windows-1252
- Latin-1
- ANSI
- Windows Western European

See `Python Standard Encoding <https://docs.python.org/3/library/codecs.html#standard-encodings>`_ for more encodings

|

Example Excel (US / comma seperated)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dialect Defaults:

.. code :: python

    delimiter = ','
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\\r\\n'
    quoting = QUOTE_MINIMAL

Usage in Robot Framework

.. code :: robotframework

    *** Settings ***
    Library    DataDriver    my_data_file.csv    dialect=excel    encoding=${None}

|

Example Excel Tab (\\\\t seperated)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dialect Defaults:

.. code :: python

    delimiter = '\\t'
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\\r\\n'
    quoting = QUOTE_MINIMAL

Usage in Robot Framework

.. code :: robotframework

    *** Settings ***
    Library    DataDriver    my_data_file.csv    dialect=excel_tab

|

Example Unix Dialect
^^^^^^^^^^^^^^^^^^^^

Dialect Defaults:

.. code :: python

    delimiter = ','
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\\n'
    quoting = QUOTE_ALL

Usage in Robot Framework

.. code :: robotframework

    *** Settings ***
    Library    DataDriver    my_data_file.csv    dialect=unix_dialect

|

Example User Defined
^^^^^^^^^^^^^^^^^^^^

User may define the format completely free.
If an option is not set, the default values are used.
To register a userdefined format user have to set the
option ``dialect`` to ``UserDefined``


Usage in Robot Framework

.. code :: robotframework

    *** Settings ***
    Library    DataDriver    my_data_file.csv
    ...    dialect=UserDefined
    ...    delimiter=.
    ...    lineterminator=\\n


|

Limitation
~~~~~~~~~~

|

Eclipse plug-in RED
^^^^^^^^^^^^^^^^^^^

There are known issues if the Eclipse plug-in RED is used. Because the
debugging Listener of this tool pre-calculates the number of test cases
before the creation of test cases by the Data Driver. This leads to the
situation that the RED listener throws exceptions because it is called
for each test step but the RED GUI already stopped debugging so that the
listener cannot send Information to the GUI. This does not influence the
execution in any way but produces a lot of unwanted exceptions in the
Log.

|

Variable types
^^^^^^^^^^^^^^

In this early Version of DataDriver, only scalar variables are
supported. Lists and dictionaries may be added in the next releases.

|

MS Excel and typed cells
^^^^^^^^^^^^^^^^^^^^^^^^

Microsoft Excel xls or xlsx file have the possibility to type thair data
cells. Numbers are typically of the type float. If these data are not
explicitly defined as text in Excel, pandas will read it as the type
that is has in excel. Because we have to work with strings in Robot
Framework these data are converted to string. This leads to the
situation that a European time value like "04.02.2019" (4th January
2019) is handed over to Robot Framework in Iso time "2019-01-04
00:00:00". This may cause unwanted behavior. To mitigate this risk you
should define Excel based files explicitly as text within Excel.

|

How to activate the Data Driver
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To activate the DataDriver for a test suite (one specific \*.robot file)
just import it as a library. You may also specify some options if the
default parameters do not fit your needs.

**Example**:

.. code :: robotframework

    *** Settings ***
    Library          DataDriver
    Test Template    Invalid Logins

|

Structure of test suite
-----------------------

|

Requirements
~~~~~~~~~~~~

In the Moment there are some requirements how a test
suite must be structured so that the DataDriver can get all the
information it needs.

 - only the first test case will be used as a template. All other test
   cases will be deleted.
 - Test cases have to be defined with a
   ``Test Template``. Reason for this is, that the DataDriver needs to
   know the names of the test case arguments. Test cases do not have
   named arguments. Keywords do.
 - The keyword which is used as
   ``Test Template`` must be defined within the test suite (in the same
   \*.robot file). If the keyword which is used as ``Test Template`` is
   defined in a ``Resource`` the DataDriver has no access to its
   arguments names.

|

Example Test Suite
~~~~~~~~~~~~~~~~~~

.. code :: robotframework

    ***Settings***
    Library           DataDriver
    Resource          login_resources.robot
    Suite Setup       Open my Browser
    Suite Teardown    Close Browsers
    Test Setup        Open Login Page
    Test Template     Invalid Login

    *** Test Case ***
    Login with user ${username} and password ${password}    Default    UserData

    ***** *Keywords* *****
    Invalid login
        [Arguments]    ${username}    ${password}
        Input username    ${username}
        Input pwd    ${password}
        click login button
        Error page should be visible

In this example, the DataDriver is activated by using it as a Library.
It is used with default settings.
As ``Test Template`` the keyword ``Invalid Login`` is used. This
keyword has two arguments. Argument names are ``${username}`` and
``${password}``. These names have to be in the CSV file as column
header. The test case has two variable names included in its name,
which does not have any functionality in Robot Framework. However, the
Data Driver will use the test case name as a template name and
replaces the variables with the specific value of the single generated
test case.
This template test will only be used as a template. The specified data
``Default`` and ``UserData`` would only be used if no CSV file has
been found.

|

Structure of data file
----------------------

|

min. required columns
~~~~~~~~~~~~~~~~~~~~~

-  ``*** Test Cases ***`` column has to be the first one.
-  *Argument columns:* For each argument of the ``Test Template``
   keyword one column must be existing in the data file as data source.
   The name of this column must match the variable name and syntax.

|

optional columns
~~~~~~~~~~~~~~~~

-  *[Tags]* column may be used to add specific tags to a test case. Tags
   may be comma separated.
-  *[Documentation]* column may be used to add specific test case
   documentation.

|

Example Data file
~~~~~~~~~~~~~~~~~

+-------------+-------------+-------------+-------------+-------------+
| \**\* Test  | ${username} | ${password} | [Tags]      | [Documentat |
| Cases \**\* |             |             |             | ion]        |
|             |             |             |             |             |
+=============+=============+=============+=============+=============+
| Right user  | demo        | ${EMPTY}    | 1           | This is a   |
| empty pass  |             |             |             | test case   |
|             |             |             |             | documentati |
|             |             |             |             | on          |
|             |             |             |             | of the      |
|             |             |             |             | first one.  |
+-------------+-------------+-------------+-------------+-------------+
| Right user  | demo        | FooBar      | 2           |             |
| wrong pass  |             |             |             |             |
+-------------+-------------+-------------+-------------+-------------+
| empty user  | ${EMPTY}    | mode        | 1,2,3,4     | This test   |
| mode pass   |             |             |             | case has    |
|             |             |             |             | the Tags    |
|             |             |             |             | 1,2,3 and 4 |
|             |             |             |             | assigned.   |
+-------------+-------------+-------------+-------------+-------------+
|             | ${EMPTY}    | ${EMPTY}    |             | This test   |
|             |             |             |             | case has a  |
|             |             |             |             | generated   |
|             |             |             |             | name based  |
|             |             |             |             | on template |
|             |             |             |             | name.       |
+-------------+-------------+-------------+-------------+-------------+
|             | ${EMPTY}    | FooBar      |             | This test   |
|             |             |             |             | case has a  |
|             |             |             |             | generated   |
|             |             |             |             | name based  |
|             |             |             |             | on template |
|             |             |             |             | name.       |
+-------------+-------------+-------------+-------------+-------------+
|             | FooBar      | mode        |             | This test   |
|             |             |             |             | case has a  |
|             |             |             |             | generated   |
|             |             |             |             | name based  |
|             |             |             |             | on template |
|             |             |             |             | name.       |
+-------------+-------------+-------------+-------------+-------------+
|             | FooBar      | ${EMPTY}    |             | This test   |
|             |             |             |             | case has a  |
|             |             |             |             | generated   |
|             |             |             |             | name based  |
|             |             |             |             | on template |
|             |             |             |             | name.       |
+-------------+-------------+-------------+-------------+-------------+
|             | FooBar      | FooBar      |             | This test   |
|             |             |             |             | case has a  |
|             |             |             |             | generated   |
|             |             |             |             | name based  |
|             |             |             |             | on template |
|             |             |             |             | name.       |
+-------------+-------------+-------------+-------------+-------------+

In this data file, eight test cases are defined. Each line specifies one
test case. The first two test cases have specific names. The other six
test cases will generate names based on template test cases name with
the replacement of variables in this name. The order of columns is
irrelevant except the first column, ``*** Test Cases ***``

|

Data Sources
------------

|

CSV / TSV (Character-separated values)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default DataDriver reads csv files. With the `Encoding and CSV
Dialect <#EncodingandCSVDialect>`__ settings you may configure which
structure your data source has.

|

XLS / XLSX Files
~~~~~~~~~~~~~~~~

If you want to use Excel based data sources, you may just set the file
to the extention or you may point to the correct file. If the extention
is ".xls" or ".xlsx" DataDriver will interpret it as Excel file.
You may select the sheet which will be read by the option ``sheet_name``.
By default it is set to 0 which will be the first table sheet.
You may use sheet index (0 is first sheet) or sheet name(case sensitive).
XLS interpreter will ignore all other options like encoding, delimiters etc.

.. code :: robotframework

    *** Settings ***
    Library    DataDriver    .xlsx

or:

.. code :: robotframework

    *** Settings ***
    Library    DataDriver    file=my_data_source.xlsx    sheet_name=2nd Sheet

|

PICT (Pairwise Independent Combinatorial Testing)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pict is able to generate data files based on a model file.
https://github.com/Microsoft/pict

Documentation: https://github.com/Microsoft/pict/blob/master/doc/pict.md

|

Requirements
^^^^^^^^^^^^

-  Path to pict.exe must be set in the %PATH% environment variable.
-  Data model file has the file extention ".pict"
-  Pict model file must be encoded in UTF-8

|

How it works
^^^^^^^^^^^^

If the file option is set to a file with the extention pict, DataDriver
will hand over this file to pict.exe and let it automatically generates
a file with the extention ".pictout". This file will the be used as data
source for the test generation. (It is tab seperated and UTF-8 encoded)
Except the file option all other options of the library will be ignored.

.. code :: robotframework

    *** Settings ***
    Library    DataDriver    my_model_file.pict

|

CSV Encoding and CSV Dialect
----------------------------

CSV is far away from well designed and has absolutely no "common"
format. Therefore it is possible to define your own dialect or use
predefined. The default is Excel-EU which is a semicolon separated
file.
These Settings are changeable as options of the Data Driver Library.

|

file=
~~~~~

.. code :: robotframework

    *** Settings ***
    Library         DataDriver    file=../data/my_data_source.csv


-  None(default): Data Driver will search in the test suites folder if a
   \*.csv file with the same name than the test suite \*.robot file exists
-  only file extention: if you just set a file extentions like ".xls" or
   ".xlsx" DataDriver will search
-  absolute path: If an absolute path to a file is set, DataDriver tries
   to find and open the given data file.
-  relative path: If the option does not point to a data file as an
   absolute path, Data Driver tries to find a data file relative to the
   folder where the test suite is located.

|

encoding=
~~~~~~~~~

may set the encoding of the CSV file. i.e.
``cp1252, ascii, iso-8859-1, latin-1, utf_8, utf_16, utf_16_be, utf_16_le``,
etc… https://docs.python.org/3.7/library/codecs.html#standard-encodings

|

dialect=
~~~~~~~~

You may change the CSV Dialect here. If the Dialect is set to
‘UserDefined’ the following options are used. Otherwise, they are
ignored.
supported Dialects are:

.. code:: python

    "excel"
        delimiter = ','
        quotechar = '"'
        doublequote = True
        skipinitialspace = False
        lineterminator = '\\r\\n'
        quoting = QUOTE_MINIMAL

    "excel-tab"
        delimiter = '\\t'

    "unix"
        delimiter = ','
        quotechar = '"'
        doublequote = True
        skipinitialspace = False
        lineterminator = '\\n'
        quoting = QUOTE_ALL


Defaults:
~~~~~~~~~

.. code:: python

    file=None,
    encoding='cp1252',
    dialect='Excel-EU',
    delimiter=';',
    quotechar='"',
    escapechar='\\\\',
    doublequote=True,
    skipinitialspace=False,
    lineterminator='\\r\\n',
    sheet_name=0


    """
    ROBOT_LIBRARY_DOC_FORMAT = 'reST'

    ROBOT_LISTENER_API_VERSION = 3
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self,
                 file=None,
                 encoding='cp1252',
                 dialect='Excel-EU',
                 delimiter=';',
                 quotechar='"',
                 escapechar='\\',
                 doublequote=True,
                 skipinitialspace=False,
                 lineterminator='\r\n',
                 sheet_name=0,
                 reader_class=None,
                 file_search_strategy='PATH',
                 file_regex=f'(?i)(.*?)(\.csv)',
                 include_tags=None
                 ):
        """**Example:**

.. code :: robotframework

    *** Settings ***
    Library    DataDriver

Options
~~~~~~~

.. code :: robotframework

    *** Settings ***
    Library    DataDriver
    ...    file=None
    ...    encoding=cp1252
    ...    dialect=Excel-EU
    ...    delimiter=;
    ...    quotechar="
    ...    escapechar=\\\\
    ...    doublequote=True
    ...    skipinitialspace=False
    ...    lineterminator=\\r\\n
    ...    sheet_name=0


|

Encoding
^^^^^^^^

``encoding`` must be set if it shall not be cp1252

**cp1252** is the same like:

- Windows-1252
- Latin-1
- ANSI
- Windows Western European

See `Python Standard Encoding <https://docs.python.org/3/library/codecs.html#standard-encodings>`_ for more encodings

|

Example Excel (US / comma seperated)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dialect Defaults:

.. code :: python

    delimiter = ','
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\\r\\n'
    quoting = QUOTE_MINIMAL

Usage in Robot Framework

.. code :: robotframework

    *** Settings ***
    Library    DataDriver    my_data_file.csv    dialect=excel    encoding=${None}

|

Example Excel Tab (\\\\t seperated)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dialect Defaults:

.. code :: python

    delimiter = '\\t'
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\\r\\n'
    quoting = QUOTE_MINIMAL

Usage in Robot Framework

.. code :: robotframework

    *** Settings ***
    Library    DataDriver    my_data_file.csv    dialect=excel_tab

|

Example Unix Dialect
^^^^^^^^^^^^^^^^^^^^

Dialect Defaults:

.. code :: python

    delimiter = ','
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\\n'
    quoting = QUOTE_ALL

Usage in Robot Framework

.. code :: robotframework

    *** Settings ***
    Library    DataDriver    my_data_file.csv    dialect=unix_dialect

|

Example User Defined
^^^^^^^^^^^^^^^^^^^^

User may define the format completely free.
If an option is not set, the default values are used.
To register a userdefined format user have to set the
option ``dialect`` to ``UserDefined``


Usage in Robot Framework

.. code :: robotframework

    *** Settings ***
    Library    DataDriver    my_data_file.csv
    ...    dialect=UserDefined
    ...    delimiter=.
    ...    lineterminator=\\n

        """
        self.ROBOT_LIBRARY_LISTENER = self

        try:
            re.compile(file_regex)
        except re.error as e:
            file_regex = r'(?i)(.*?)(\.csv)'
            BuiltIn().log_to_console(f'[ DataDriver ] invalid Regex! used {file_regex} instead.')
            BuiltIn().log_to_console(e)

        self.reader_config = ReaderConfig(
            file=file,
            encoding=encoding,
            dialect=dialect,
            delimiter=delimiter,
            quotechar=quotechar,
            escapechar=escapechar,
            doublequote=doublequote,
            skipinitialspace=skipinitialspace,
            lineterminator=lineterminator,
            sheet_name=sheet_name,
            reader_class=reader_class,
            file_search_strategy=file_search_strategy.upper(),
            file_regex=file_regex
        )

        self.suite_source = None
        self.template_test = None
        self.template_keyword = None
        self.data_table = None
        self.index = None
        self.test_case_data = TestCaseData()
        self.include_tags = None
        if include_tags:
            self.include_tags = set([t.strip() for t in include_tags.split(",")])

    def _start_suite(self, suite, result):
        """Called when a test suite starts.
        Data and result are model objects representing the executed test suite and its execution results, respectively.

        :param suite: class robot.running.model.TestSuite(name='', doc='', metadata=None, source=None)
        :param result: NOT USED
        """
        self.loglevel = BuiltIn().get_variable_value('${LOG LEVEL}')

        self.suite_source = suite.source
        self._create_data_table()
        self.template_test = suite.tests[0]
        self.template_keyword = self._get_template_keyword(suite)
        temp_test_list = list()
        for self.index, self.test_case_data in enumerate(self.data_table):
            if self.include_tags and not set(self.test_case_data.tags).intersection(self.include_tags):
                continue
            self._create_test_from_template()
            temp_test_list.append(self.test)
        suite.tests = temp_test_list

    def _create_data_table(self):
        """
        this function creates a dictionary which contains all data from data file.
        Keys are header names.
        Values are data of this column as array.
        """
        self._resolve_file_attribute()

        self.data_table = self._data_reader().get_data_from_source()
        if self.loglevel == 'DEBUG':
            BuiltIn().log_to_console(f"[ DataDriver ] Opening file '{self.reader_config.file}'")
            BuiltIn().log_to_console(f'[ DataDriver ] {len(self.data_table)}'
                                     f' Test Cases loaded...')

    def _data_reader(self):
        if not self.reader_config.reader_class:
            reader = self._get_data_reader_from_file_extension()
        else:
            reader = self._get_data_reader_from_reader_class()
        return reader

    def _get_data_reader_from_file_extension(self):
        filename, file_extension = os.path.splitext(self.reader_config.file)
        reader_type = file_extension.lower()[1:]
        if self.loglevel == 'DEBUG':
            BuiltIn().log_to_console(f'[ DataDriver ] Initialized in {reader_type}-mode.')
        reader_module = importlib.import_module(f'..{reader_type}_reader', 'DataDriver.DataDriver')
        if self.loglevel == 'DEBUG':
            BuiltIn().log_to_console(f'[ DataDriver ] Reader Module: {reader_module}')
        reader_class = getattr(reader_module, f'{reader_type}_Reader')

        reader = reader_class(self.reader_config)
        return reader

    def _get_data_reader_from_reader_class(self):
        reader_name = self.reader_config.reader_class
        if self.loglevel == 'DEBUG':
            BuiltIn().log_to_console(f'[ DataDriver ] Initializes  {reader_name}')
        reader_module = importlib.import_module(f'..{reader_name}', 'DataDriver.DataDriver')
        if self.loglevel == 'DEBUG':
            BuiltIn().log_to_console(f'[ DataDriver ] Reader Module: {reader_module}')
        reader_class = getattr(reader_module, f'{reader_name}')
        if self.loglevel == 'DEBUG':
            BuiltIn().log_to_console(f'[ DataDriver ] Reader Class: {reader_class}')
        reader = reader_class(self.reader_config)
        return reader

    def _resolve_file_attribute(self):
        if self.reader_config.file_search_strategy == 'PATH':
            if (not self.reader_config.file) or ('' == self.reader_config.file[:self.reader_config.file.rfind('.')]):
                self._set_data_file_to_suite_source()
            else:
                self._check_if_file_exists_as_path_or_in_suite()
        elif self.reader_config.file_search_strategy == 'REGEX':
            self._search_file_from_regex()
        elif self.reader_config.file_search_strategy == 'EVALUATE':
            pass  # ToDo: implement other search calls
        elif self.reader_config.file_search_strategy == 'NONE':
            pass
        else:
            raise ValueError(f'file_search_strategy={self.reader_config.file_search_strategy} is not a valid value!')

    def _set_data_file_to_suite_source(self):
        if not self.reader_config.file:
            suite_path_as_data_file = f'{self.suite_source[:self.suite_source.rfind(".")]}.csv'
        else:
            suite_path = self.suite_source[:self.suite_source.rfind(".")]
            file_extension = self.reader_config.file[self.reader_config.file.rfind("."):]
            suite_path_as_data_file = f'{suite_path}{file_extension}'

        if os.path.isfile(suite_path_as_data_file):
            self.reader_config.file = suite_path_as_data_file
        else:
            raise FileNotFoundError(
                'File attribute was empty. Tried to find '
                + suite_path_as_data_file + ' but file does not exist.')

    def _check_if_file_exists_as_path_or_in_suite(self):
        if not os.path.isfile(self.reader_config.file):
            suite_dir = str(os.path.dirname(self.suite_source))
            file_in_suite_dir = os.path.join(suite_dir, self.reader_config.file)
            if os.path.isfile(file_in_suite_dir):
                self.reader_config.file = file_in_suite_dir
            else:
                raise FileNotFoundError(
                    'File attribute was not a full path. Tried to find '
                    + file_in_suite_dir + ' but file does not exist.')

    def _search_file_from_regex(self):
        if os.path.isdir(self.reader_config.file):
            for filename in os.listdir(self.reader_config.file):
                if re.match(self.reader_config.file_regex, filename):
                    self.reader_config.file = os.path.join(self.reader_config.file, filename)
                    break

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

    def _replace_test_case_name(self):
        if self.test_case_data.test_case_name == '':
            for variable_name in self.test_case_data.arguments:
                self.test.name = self.test.name.replace(variable_name, self.test_case_data.arguments[variable_name])
        else:
            self.test.name = self.test_case_data.test_case_name

    def _replace_test_case_keywords(self):
        self.test.keywords.clear()
        if self.template_test.keywords.setup is not None:
            self.test.keywords.create(name=self.template_test.keywords.setup.name, type='setup',
                                      args=self.template_test.keywords.setup.args)
        self.test.keywords.create(name=self.template_keyword.name,
                                  args=self._get_template_arguments())
        if self.template_test.keywords.teardown is not None:
            self.test.keywords.create(name=self.template_test.keywords.teardown.name, type='teardown',
                                      args=self.template_test.keywords.teardown.args)

    def _get_template_arguments(self):
        return_arguments = []
        for arg in self.template_keyword.args:
            if arg in self.test_case_data.arguments:
                return_arguments.append(self.test_case_data.arguments[arg])
                # Todo: here i have to handle the dictionaries stuff
            else:
                return_arguments.append(arg)
        return return_arguments

    def _add_test_case_tags(self):
        for tag in self.test_case_data.tags:
            self.test.tags.add(tag.strip())

    def _replace_test_case_doc(self):
        self.test.doc = self.test_case_data.documentation
