===================================================
DataDriver for Robot Framework®
===================================================

DataDriver is a Data-Driven extension for Robot Framework®.
This document explains how to use the DataDriver library listener. For
information about installation, support, and more, please visit the
`project page <https://github.com/Snooz82/robotframework-datadriver>`_

For more information about Robot Framework®, see http://robotframework.org.

DataDriver is used/imported as Library but does not provide keywords
which can be used in a test. DataDriver uses the Listener Interface
Version 3 to manipulate the test cases and creates new test cases based
on a Data-File that contains the data for Data-Driven Testing. These
data file may be .csv , .xls or .xlsx files.

Data Driver is also able to cooperate with Microsoft PICT. An Open
Source Windows tool for data combination testing. Pict is able to
generate data combinations based on textual model definitions.
https://github.com/Microsoft/pict

It is also possible to implement own DataReaders in Python to read
your test data from some other sources, like databases or json files.


Installation
------------

If you already have Python >= 3.6 with pip installed, you can simply
run:

``pip install --upgrade robotframework-datadriver``


Excel Support
~~~~~~~~~~~~~

For file support of ``xls`` or ``xlsx`` file you need to install the extra XLS or the dependencies.
It contains the dependencies of pandas, numpy and xlrd. Just add [XLS] to your installation.
New since version 3.6.

``pip install --upgrade robotframework-datadriver[XLS]``


Python 2
~~~~~~~~

or if you have Python 2 and 3 installed in parallel you may use

``pip3 install --upgrade robotframework-datadriver``

DataDriver is compatible with Python 2.7 only in Version 0.2.7.

``pip install --upgrade robotframework-datadriver==0.2.7``

Because Python 2.7 is deprecated, there are no new feature to python 2.7 compatible version.


Table of contents
-----------------

-  `What DataDriver Does`_
-  `How DataDriver Works`_
-  `Usage`_
-  `Structure of Test Suite`_
-  `Structure of data file`_
-  `Accessing Test Data From Robot Variables`_
-  `Data Sources`_
-  `File Encoding and CSV Dialect`_
-  `Custom DataReader Classes`_
-  `Selection of Test Cases to Execute`_
-  `Configure DataDriver by Pre-Run Keyword`_
-  `Pabot and DataDriver`_


What DataDriver Does
--------------------

DataDriver is an alternative approach to create Data-Driven Tests with
Robot Framework®. DataDriver creates multiple test cases based on a test
template and data content of a csv or Excel file. All created tests
share the same test sequence (keywords) and differ in the test data.
Because these tests are created on runtime only the template has to be
specified within the robot test specification and the used data are
specified in an external data file.


RoboCon 2020 Talk
~~~~~~~~~~~~~~~~~

.. image:: https://img.youtube.com/vi/RtEUr1i4x3s/0.jpg
   :target: https://www.youtube.com/watch?v=RtEUr1i4x3s

Brief overview what DataDriver is and how it works at the RoboCon 2020 in Helsiki.


Alternative approach
~~~~~~~~~~~~~~~~~~~~

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

This inbuilt approach is fine for a hand full of data and a hand full of
test cases. If you have generated or calculated data and specially if
you have a variable amount of test case / combinations these robot files
become quite a pain. With DataDriver you may write the same test case
syntax but only once and deliver the data from en external data file.

One of the rare reasons when Microsoft® Excel or LibreOffice Calc may be
used in testing… ;-)

`See example test suite <#example-suite>`__

`See example csv table <#example-csv>`__


How DataDriver Works
--------------------

When the DataDriver is used in a test suite it will be activated before
the test suite starts. It uses the Listener Interface Version 3 of Robot
Framework® to read and modify the test specification objects. After
activation it searches for the ``Test Template`` -Keyword to analyze the
``[Arguments]`` it has. As a second step, it loads the data from the
specified data source. Based on the ``Test Template`` -Keyword, DataDriver
creates as much test cases as data sets are in the data source.

In the case that data source is csv (Default)
As values for the arguments of the ``Test Template`` -Keyword, DataDriver
reads values from the column of the CSV file with the matching name of the
``[Arguments]``.
For each line of the CSV data table, one test case will be created. It
is also possible to specify test case names, tags and documentation for
each test case in the specific test suite related CSV file.


Usage
-----

Data Driver is a "Library Listener" but does not provide keywords.
Because Data Driver is a listener and a library at the same time it
sets itself as a listener when this library is imported into a test suite.

To use it, just use it as Library in your suite. You may use the first
argument (option) which may set the file name or path to the data file.

Without any options set, it loads a .csv file which has the same name
and path like the test suite .robot .



**Example:**

.. code :: robotframework

    *** Settings ***
    Library    DataDriver
    Test Template    Invalid Logins

    *** Keywords ***
    Invalid Logins
        ...


Structure of Test Suite
-----------------------


Requirements
~~~~~~~~~~~~

In the Moment there are some requirements how a test
suite must be structured so that the DataDriver can get all the
information it needs.

 - only the first test case will be used as a template. All other test
   cases will be deleted.
 - Test cases have to be defined with a
   ``Test Template`` in Settings secion. Reason for this is,
   that the DataDriver needs to know the names of the test case arguments.
   Test cases do not have named arguments. Keywords do.
 - The keyword which is used as
   ``Test Template`` must be defined within the test suite (in the same
   \*.robot file). If the keyword which is used as ``Test Template`` is
   defined in a ``Resource`` the DataDriver has no access to its
   arguments names.


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
which does not have any functionality in Robot Framework®. However, the
Data Driver will use the test case name as a template name and
replaces the variables with the specific value of the single generated
test case.
This template test will only be used as a template. The specified data
``Default`` and ``UserData`` would only be used if no CSV file has
been found.


Structure of data file
----------------------


min. required columns
~~~~~~~~~~~~~~~~~~~~~

-  ``*** Test Cases ***`` column has to be the first one.
-  *Argument columns:* For each argument of the ``Test Template``
   keyword one column must be existing in the data file as data source.
   The name of this column must match the variable name and syntax.


optional columns
~~~~~~~~~~~~~~~~

-  *[Tags]* column may be used to add specific tags to a test case. Tags
   may be comma separated.
-  *[Documentation]* column may be used to add specific test case
   documentation.


Example Data file
~~~~~~~~~~~~~~~~~

+-------------+-------------+-------------+-------------+------------------+
| \**\* Test  | ${username} | ${password} | [Tags]      | [Documentation]  |
| Cases \**\* |             |             |             |                  |
|             |             |             |             |                  |
+=============+=============+=============+=============+==================+
| Right user  | demo        | ${EMPTY}    | 1           | This is a test   |
| empty pass  |             |             |             | case             |
|             |             |             |             | documentation of |
|             |             |             |             | the first one.   |
+-------------+-------------+-------------+-------------+------------------+
| Right user  | demo        | FooBar      | 2,3,foo     | This test        |
| wrong pass  |             |             |             | case has         |
|             |             |             |             | the Tags         |
|             |             |             |             | 2,3 and foo      |
|             |             |             |             | assigned.        |
+-------------+-------------+-------------+-------------+------------------+
|             | ${EMPTY}    | mode        | 1,2,3,4     | This test        |
|             |             |             |             | case has a       |
|             |             |             |             | generated        |
|             |             |             |             | name based       |
|             |             |             |             | on template      |
|             |             |             |             | name.            |
+-------------+-------------+-------------+-------------+------------------+
|             | ${EMPTY}    | ${EMPTY}    |             |                  |
+-------------+-------------+-------------+-------------+------------------+
|             | ${EMPTY}    | FooBar      |             |                  |
+-------------+-------------+-------------+-------------+------------------+
|             | FooBar      | mode        |             |                  |
+-------------+-------------+-------------+-------------+------------------+
|             | FooBar      | ${EMPTY}    |             |                  |
+-------------+-------------+-------------+-------------+------------------+
|             | FooBar      | FooBar      |             |                  |
+-------------+-------------+-------------+-------------+------------------+

In this data file, eight test cases are defined. Each line specifies one
test case. The first two test cases have specific names. The other six
test cases will generate names based on template test cases name with
the replacement of variables in this name. The order of columns is
irrelevant except the first column, ``*** Test Cases ***``

Supported Data Types
~~~~~~~~~~~~~~~~~~~~

In general DataDriver supports any Object that is handed over from the DataReader.
However the text based readers for csv, excel and so do support different types as well.
DataDriver supports Robot Framework® Scalar variables as well as Dictionaries and Lists.
It also support python literal evaluations.

Scalar Variables
^^^^^^^^^^^^^^^^

The Prefix ``$`` defines that the value in the cell is taken as in Robot Framework® Syntax.
``String`` is ``str``, ``${1}`` is ``int`` and ``${None}`` is NoneType.
The Prefix only defines the value typ. It can also be used to assign a scalar to a dictionary key.
See example table: ``${user}[id]``


Dictionary Variables
^^^^^^^^^^^^^^^^^^^^

Dictionaries can be created in different ways.

One option is, to use the prefix ``&``.
If a variable is defined that was (i.e. ``&{dict}``) the cell value is interpreted the same way,
the BuiltIn keyword `Create Dictionary <https://robotframework.org/robotframework/latest/libraries/BuiltIn.html#Create%20Dictionary>`_ would do.
The arguments here are comma (``,``) separated.
See example table: ``&{dict}``

The other option is to define scalar variables in dictionary syntax like ``${user}[name]`` or ``${user.name}``
That can be also nested dictionaries. DataDriver will create Robot Framework® (DotDict) Dictionaries, that can be accessed with ``${user.name.first}``
See example table: ``${user}[name][first]``


List Variables
^^^^^^^^^^^^^^

Lists can be created with the prefix ``@`` as comma (``,``) separated list.
See example table: ``@{list}``

Be aware that a list with an empty string has to be the cell content `${Empty}`.

Python Literals
^^^^^^^^^^^^^^^

DataDriver can evaluate Literals.
It uses the prefix ``e`` for that. (i.e. ``e{list_eval}``)
For that it uses `BuiltIn Evaluate <https://robotframework.org/robotframework/latest/libraries/BuiltIn.html#Evaluate>`_

See example table: ``e{user.chk}``


+--------------------------+-----------------------+---------------+-------------------------+-----------------------------+------------------------------------------+--------------------------+-------------------+-------------------+----------------------------+-------------------------+------------------------------------------------------------------+
|  ``*** Test Cases ***``  |  ``${scalar}``        |  ``@{list}``  |  ``e{list_eval}``       |  ``&{dict}``                |  ``e{dict_eval}``                        |  ``e{eval}``             |  ``${exp_eval}``  |  ``${user}[id]``  |  ``${user}[name][first]``  |  ``${user.name.last}``  |  ``e{user.chk}``                                                 |
+--------------------------+-----------------------+---------------+-------------------------+-----------------------------+------------------------------------------+--------------------------+-------------------+-------------------+----------------------------+-------------------------+------------------------------------------------------------------+
|  ``One``                 |  ``Sum List``         |  ``1,2,3,4``  |  ``["1","2","3","4"]``  |  ``key=value``              |  ``{'key': 'value'}``                    |  ``[1,2,3,4]``           |  ``10``           |  ``1``            |  ``Pekka``                 |  ``Klärck``             |  ``{'id': '1', 'name': {'first': 'Pekka', 'last': 'Klärck'}}``   |
+--------------------------+-----------------------+---------------+-------------------------+-----------------------------+------------------------------------------+--------------------------+-------------------+-------------------+----------------------------+-------------------------+------------------------------------------------------------------+
|  ``Two``                 |  ``Should be Equal``  |  ``a,b,c,d``  |  ``["a","b","c","d"]``  |  ``key,value``              |  ``{'key': 'value'}``                    |  ``True``                |  ``${true}``      |  ``2``            |  ``Ed``                    |  ``Manlove``            |  ``{'id': '2', 'name': {'first': 'Ed', 'last': 'Manlove'}}``     |
+--------------------------+-----------------------+---------------+-------------------------+-----------------------------+------------------------------------------+--------------------------+-------------------+-------------------+----------------------------+-------------------------+------------------------------------------------------------------+
|  ``Three``               |  ``Whos your Daddy``  |  ``!,",',$``  |  ``["!",'"',"'","$"]``  |  ``z,value,a,value2``       |  ``{'a': 'value2', 'z': 'value'}``       |  ``{'Daddy' : 'René'}``  |  ``René``         |  ``3``            |  ``Tatu``                  |  ``Aalto``              |  ``{'id': '3', 'name': {'first': 'Tatu', 'last': 'Aalto'}}``     |
+--------------------------+-----------------------+---------------+-------------------------+-----------------------------+------------------------------------------+--------------------------+-------------------+-------------------+----------------------------+-------------------------+------------------------------------------------------------------+
|  ``4``                   |  ``Should be Equal``  |  ``1``        |  ``["1"]``              |  ``key=value``              |  ``{'key': 'value'}``                    |  ``1``                   |  ``${1}``         |  ``4``            |  ``Jani``                  |  ``Mikkonen``           |  ``{'id': '4', 'name': {'first': 'Jani', 'last': 'Mikkonen'}}``  |
+--------------------------+-----------------------+---------------+-------------------------+-----------------------------+------------------------------------------+--------------------------+-------------------+-------------------+----------------------------+-------------------------+------------------------------------------------------------------+
|  ``5``                   |  ``Should be Equal``  |               |  ``[]``                 |  ``a=${2}``                 |  ``{'a':2}``                             |  ``"string"``            |  ``string``       |  ``5``            |  ``Mikko``                 |  ``Korpela``            |  ``{'id': '5', 'name': {'first': 'Mikko', 'last': 'Korpela'}}``  |
+--------------------------+-----------------------+---------------+-------------------------+-----------------------------+------------------------------------------+--------------------------+-------------------+-------------------+----------------------------+-------------------------+------------------------------------------------------------------+
|  ``6``                   |  ``Should be Equal``  |  ``[1,2]``    |  ``["[1","2]"]``        |  ``key=value,key2=value2``  |  ``{'key': 'value', 'key2': 'value2'}``  |  ``None``                |  ``${none}``      |  ``6``            |  ``Ismo``                  |  ``Aro``                | ``{'id': '6', 'name': {'first': 'Ismo', 'last': 'Aro'}}``        |
+--------------------------+-----------------------+---------------+-------------------------+-----------------------------+------------------------------------------+--------------------------+-------------------+-------------------+----------------------------+-------------------------+------------------------------------------------------------------+


Accessing Test Data From Robot Variables
----------------------------------------

If neccesary it is possible to access the fetched data tables directly from a Robot Framework® variable.
This could be helpfull in Test Setup or in Suite Setup.

There are three variables available within the Data-Driven Suite:

@{DataDriver_DATA_LIST}
~~~~~~~~~~~~~~~~~~~~~~~

A list as suite variable containing a robot dictionary for each test case that is selected for execution.

.. code :: json

    [
      {
        "test_case_name": "Right user empty pass",
        "arguments": {
          "${username}": "demo",
          "${password}": "${EMPTY}"
        },
        "tags": [
          "1"
        ],
        "documentation": "This is a test case documentation of the first one."
      },
      {
        "test_case_name": "Right user wrong pass",
        "arguments": {
          "${username}": "demo",
          "${password}": "FooBar"
        },
        "tags": [
          "2",
          "3",
          "foo"
        ],
        "documentation": "This test case has the Tags 2,3 and foo"
      },
      {
        "test_case_name": "Login with user '${EMPTY}' and password 'mode'",
        "arguments": {
          "${username}": "${EMPTY}",
          "${password}": "mode"
        },
        "tags": [
          "1",
          "2",
          "3",
          "4"
        ],
        "documentation": "This test case has a generated name based on template name."
      },
      {
        "test_case_name": "Login with user '${EMPTY}' and password '${EMPTY}'",
        "arguments": {
          "${username}": "${EMPTY}",
          "${password}": "${EMPTY}"
        },
        "tags": [
          ""
        ],
        "documentation": ""
      },
      {
        "test_case_name": "Login with user '${EMPTY}' and password 'FooBar'",
        "arguments": {
          "${username}": "${EMPTY}",
          "${password}": "FooBar"
        },
        "tags": [
          ""
        ],
        "documentation": ""
      },
      {
        "test_case_name": "Login with user 'FooBar' and password 'mode'",
        "arguments": {
          "${username}": "FooBar",
          "${password}": "mode"
        },
        "tags": [
          "foo",
          "1"
        ],
        "documentation": ""
      },
      {
        "test_case_name": "Login with user 'FooBar' and password '${EMPTY}'",
        "arguments": {
          "${username}": "FooBar",
          "${password}": "${EMPTY}"
        },
        "tags": [
          "foo"
        ],
        "documentation": ""
      },
      {
        "test_case_name": "Login with user 'FooBar' and password 'FooBar'",
        "arguments": {
          "${username}": "FooBar",
          "${password}": "FooBar"
        },
        "tags": [
          "foo",
          "2"
        ],
        "documentation": ""
      }
    ]

This can be accessed as usual in Robot Framework®.

``${DataDriver_DATA_LIST}[2][arguments][\\${password}]`` would result in ``mode`` .



&{DataDriver_DATA_DICT}
~~~~~~~~~~~~~~~~~~~~~~~

A dictionary as suite variable that contains the same data as the list, with the test names as keys.

.. code :: json

    {
      "Right user empty pass": {
        "test_case_name": "Right user empty pass",
        "arguments": {
          "${username}": "demo",
          "${password}": "${EMPTY}"
        },
        "tags": [
          "1"
        ],
        "documentation": "This is a test case documentation of the first one."
      },
      "Right user wrong pass": {
        "test_case_name": "Right user wrong pass",
        "arguments": {
          "${username}": "demo",
          "${password}": "FooBar"
        },
        "tags": [
          "2",
          "3",
          "foo"
        ],
        "documentation": "This test case has the Tags 2,3 and foo"
      },
      "Login with user '${EMPTY}' and password 'mode'": {
        "test_case_name": "Login with user '${EMPTY}' and password 'mode'",
        "arguments": {
          "${username}": "${EMPTY}",
          "${password}": "mode"
        },
        "tags": [
          "1",
          "2",
          "3",
          "4"
        ],
        "documentation": "This test case has a generated name based on template name."
      },
      "Login with user '${EMPTY}' and password '${EMPTY}'": {
        "test_case_name": "Login with user '${EMPTY}' and password '${EMPTY}'",
        "arguments": {
          "${username}": "${EMPTY}",
          "${password}": "${EMPTY}"
        },
        "tags": [
          ""
        ],
        "documentation": ""
      },
      "Login with user '${EMPTY}' and password 'FooBar'": {
        "test_case_name": "Login with user '${EMPTY}' and password 'FooBar'",
        "arguments": {
          "${username}": "${EMPTY}",
          "${password}": "FooBar"
        },
        "tags": [
          ""
        ],
        "documentation": ""
      },
      "Login with user 'FooBar' and password 'mode'": {
        "test_case_name": "Login with user 'FooBar' and password 'mode'",
        "arguments": {
          "${username}": "FooBar",
          "${password}": "mode"
        },
        "tags": [
          "foo",
          "1"
        ],
        "documentation": ""
      },
      "Login with user 'FooBar' and password '${EMPTY}'": {
        "test_case_name": "Login with user 'FooBar' and password '${EMPTY}'",
        "arguments": {
          "${username}": "FooBar",
          "${password}": "${EMPTY}"
        },
        "tags": [
          "foo"
        ],
        "documentation": ""
      },
      "Login with user 'FooBar' and password 'FooBar'": {
        "test_case_name": "Login with user 'FooBar' and password 'FooBar'",
        "arguments": {
          "${username}": "FooBar",
          "${password}": "FooBar"
        },
        "tags": [
          "foo",
          "2"
        ],
        "documentation": ""
      }
    }

&{DataDriver_TEST_DATA}
~~~~~~~~~~~~~~~~~~~~~~~

A dictionary as test variable that contains the test data of the current test case.
This dictionary does also contain arguments that are not used in the ``Test Template`` keyword.
This can be used in Test Setup and within a test case.

.. code :: json

    {
      "test_case_name": "Right user wrong pass",
      "arguments": {
        "${username}": "demo",
        "${password}": "FooBar"
      },
      "tags": [
        "2",
        "3",
        "foo"
      ],
      "documentation": "This test case has the Tags 2,3 and foo"
    }


Data Sources
------------


CSV / TSV (Character-separated values)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default DataDriver reads csv files. With the `Encoding and CSV
Dialect <#file-encoding-and-csv-dialect>`__ settings you may configure which
structure your data source has.


XLS / XLSX Files
~~~~~~~~~~~~~~~~

To use Excel file types, you have to install DataDriver with the Extra XLS.

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


MS Excel and typed cells
^^^^^^^^^^^^^^^^^^^^^^^^

Microsoft Excel xls or xlsx file have the possibility to type thair data
cells. Numbers are typically of the type float. If these data are not
explicitly defined as text in Excel, pandas will read it as the type
that is has in excel. Because we have to work with strings in Robot
Framework® these data are converted to string. This leads to the
situation that a European time value like "04.02.2019" (4th January
2019) is handed over to Robot Framework® in Iso time "2019-01-04
00:00:00". This may cause unwanted behavior. To mitigate this risk you
should define Excel based files explicitly as text within Excel.

Alternatively you may deactivate that string conversion.
To do so, you have to add the option ``preserve_xls_types`` to ``True``.
In that case, you will get str, float, boolean, int, datetime.time,
datetime.datetime and some others.

.. code :: robotframework

    *** Settings ***
    Library    DataDriver    file=my_data_source.xlsx    preserve_xls_types=True

PICT (Pairwise Independent Combinatorial Testing)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pict is able to generate data files based on a model file.
https://github.com/Microsoft/pict

Documentation: https://github.com/Microsoft/pict/blob/master/doc/pict.md


Requirements
^^^^^^^^^^^^

-  Path to pict.exe must be set in the %PATH% environment variable.
-  Data model file has the file extention ".pict"
-  Pict model file must be encoded in UTF-8


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


Glob File Pattern
~~~~~~~~~~~~~~~~~

This module implements a reader class that creates a test case for each file or folder that matches the given glob pattern.

With an optional argument "arg_name" you can modify the argument that will be set. See folder example.

Example with json files:

.. code :: robotframework

    *** Settings ***
    Library           DataDriver    file=${CURDIR}/DataFiles/*_File.json    reader_class=glob_reader
    Library           OperatingSystem
    Test Template     Test all Files


    *** Test Cases ***
    Glob_Reader_Test    Wrong_File.NoJson


    *** Keywords ***
    Test all Files
        [Arguments]    ${file_name}
        ${file_content}=    Get File    ${file_name}
        ${content}=    Evaluate    json.loads($file_content)["test_case"]
        Should Be Equal    ${TEST_NAME}    ${content}


Example with folders:

.. code :: robotframework

    *** Settings ***
    Library           DataDriver    file=${CURDIR}/FoldersToFind/*/    reader_class=glob_reader    arg_name=\\${folder_name}
    Library           OperatingSystem
    Test Template     Test all Files


    *** Test Cases ***
    Glob_Reader_Test    Wrong_File.NoJson


    *** Keywords ***
    Test all Files
        [Arguments]    ${folder_name}
        ${content}=    Get File    ${folder_name}/verify.txt
        Should Be Equal    ${TEST_NAME}    ${content}


File Encoding and CSV Dialect
-----------------------------

CSV is far away from well designed and has absolutely no "common"
format. Therefore it is possible to define your own dialect or use
predefined. The default is Excel-EU which is a semicolon separated
file.
These Settings are changeable as options of the Data Driver Library.


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


encoding=
~~~~~~~~~

``encoding=`` must be set if it shall not be cp1252.

**Examples**:

``cp1252, ascii, iso-8859-1, latin-1, utf_8, utf_16, utf_16_be, utf_16_le``

**cp1252** is:

- Code Page 1252
- Windows-1252
- Windows Western European

Most characters are same between ISO-8859-1 (Latin-1) except for the code points 128-159 (0x80-0x9F).
These Characters are available in cp1252 which are not present in Latin-1.

``€ ‚ ƒ „ … † ‡ ˆ ‰ Š ‹ Œ Ž ‘ ’ “ ” • – — ˜ ™ š › œ ž Ÿ``

See `Python Standard Encoding <https://docs.python.org/3/library/codecs.html#standard-encodings>`_ for more encodings


dialect=
~~~~~~~~

You may change the CSV Dialect here.
The dialect option can be one of the following:
- Excel-EU
- excel
- excel-tab
- unix
- UserDefined

supported Dialects are:

.. code:: python

    "Excel-EU"
        delimiter=';',
        quotechar='"',
        escapechar='\\',
        doublequote=True,
        skipinitialspace=False,
        lineterminator="\\r\\n",
        quoting=csv.QUOTE_ALL

    "excel"
        delimiter = ','
        quotechar = '"'
        doublequote = True
        skipinitialspace = False
        lineterminator = '\\r\\n'
        quoting = QUOTE_MINIMAL

    "excel-tab"
        delimiter = '\\t'
        quotechar = '"'
        doublequote = True
        skipinitialspace = False
        lineterminator = '\\r\\n'
        quoting = QUOTE_MINIMAL

    "unix"
        delimiter = ','
        quotechar = '"'
        doublequote = True
        skipinitialspace = False
        lineterminator = '\\n'
        quoting = QUOTE_ALL




Usage in Robot Framework®

.. code :: robotframework

    *** Settings ***
    Library    DataDriver    my_data_file.csv    dialect=excel



.. code :: robotframework

    *** Settings ***
    Library    DataDriver    my_data_file.csv    dialect=excel_tab



.. code :: robotframework

    *** Settings ***
    Library    DataDriver    my_data_file.csv    dialect=unix_dialect



Example User Defined
^^^^^^^^^^^^^^^^^^^^

User may define the format completely free.
If an option is not set, the default values are used.
To register a userdefined format user have to set the
option ``dialect`` to ``UserDefined``


Usage in Robot Framework®

.. code :: robotframework

    *** Settings ***
    Library    DataDriver    my_data_file.csv
    ...    dialect=UserDefined
    ...    delimiter=.
    ...    lineterminator=\\n




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


Custom DataReader Classes
-------------------------

It is possible to write your own DataReader Class as a plugin for DataDriver.
DataReader Classes are called from DataDriver to return a list of TestCaseData.


Using Custom DataReader
~~~~~~~~~~~~~~~~~~~~~~~

DataReader classes are loaded dynamically into DataDriver while runtime.
DataDriver identifies the DataReader to load by the file extantion of the data file or by the option ``reader_class``.


Select Reader by File Extension:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code :: robotframework

    *** Settings ***
    Library    DataDriver    file=mydata.csv

This will load the class ``csv_reader`` from ``csv_reader.py`` from the same folder.


Select Reader by Option:
^^^^^^^^^^^^^^^^^^^^^^^^

.. code :: robotframework

    *** Settings ***
        Library    DataDriver   file=mydata.csv    reader_class=generic_csv_reader    dialect=userdefined   delimiter=\\t    encoding=UTF-8

This will load the class ``generic_csv_reader`` from ``generic_csv_reader.py`` from same folder.


Create Custom Reader
~~~~~~~~~~~~~~~~~~~~

Recommendation:

Have a look to the Source Code of existing DataReader like ``csv_reader.py`` or ``generic_csv_reader.py`` .

To write your own reader, create a class inherited from ``AbstractReaderClass``.

Your class will get all available configs from DataDriver as an object of ``ReaderConfig`` on ``__init__``.

DataDriver will call the method ``get_data_from_source``
This method should then load your data from your custom source and stores them into list of object of ``TestCaseData``.
This List of ``TestCaseData`` will be returned to DataDriver.

``AbstractReaderClass`` has also some optional helper methods that may be useful.

You can either place the custom reader with the others in DataDriver folder or anywhere on the disk.
In the first case or if your custom reader is in python path just use it like the others by name:

.. code :: robotframework

    *** Settings ***
    Library          DataDriver    reader_class=my_reader

In case it is somewhere on the disk, it is possible to use an absolute or relative path to a custom Reader.
Imports of custom readers follow the same rules like importing Robot Framework® libraries.
Path can be relative to ${EXECDIR} or to DataDriver/__init__.py:


.. code :: robotframework

    *** Settings ***
    Library          DataDriver    reader_class=C:/data/my_reader.py    # set custom reader
    ...                            file_search_strategy=None            # set DataDriver to not check file
    ...                            min=0                                # kwargs arguments for custom reader
    ...                            max=62

This `my_reader.py` should implement a class inherited from AbstractReaderClass that is named `my_reader`.

.. code :: python

    from DataDriver.AbstractReaderClass import AbstractReaderClass  # inherit class from AbstractReaderClass
    from DataDriver.ReaderConfig import TestCaseData  # return list of TestCaseData to DataDriver


    class my_reader(AbstractReaderClass):

        def get_data_from_source(self):  # This method will be called from DataDriver to get the TestCaseData list.
            test_data = []
            for i in range(int(self.kwargs['min']), int(self.kwargs['max'])):  # Dummy code to just generate some data
                args = {'${var_1}': str(i), '${var_2}': str(i)}  # args is a dictionary. Variable name is the key, value is value.
                test_data.append(TestCaseData(f'test {i}', args, ['tag']))  # add a TestCaseData object to the list of tests.
            return test_data  # return the list of TestCaseData to DataDriver


See other readers as example.


Selection of Test Cases to Execute
----------------------------------

Because test cases that are created by DataDriver after parsing while execution,
it is not possible to use some Robot Framework® methods to select test cases.


Examples for options that have to be used differently:

+-------------------+-----------------------------------------------------------------------+
| robot option      | Description                                                           |
+===================+=======================================================================+
| ``--test``        | Selects the test cases by name.                                       |
+-------------------+-----------------------------------------------------------------------+
| ``--task``        | Alias for --test that can be used when executing tasks.               |
+-------------------+-----------------------------------------------------------------------+
| ``--rerunfailed`` | Selects failed tests from an earlier output file to be re-executed.   |
+-------------------+-----------------------------------------------------------------------+
| ``--include``     | Selects the test cases by tag.                                        |
+-------------------+-----------------------------------------------------------------------+
| ``--exclude``     | Selects the test cases by tag.                                        |
+-------------------+-----------------------------------------------------------------------+


Selection of test cases by name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Select a single test case:
^^^^^^^^^^^^^^^^^^^^^^^^^^

To execute just a single test case by its exact name it is possible to execute the test suite
and set the global variable ${DYNAMICTEST} with the name of the test case to execute as value.
Pattern must be ``suitename.testcasename``.

Example:

.. code ::

    robot --variable "DYNAMICTEST:my suite name.test case to be executed" my_suite_name.robot

Pabot uses this feature to execute a single test case when using ``--testlevelsplit``


Select a list of test cases:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is possible to set a list of test case names by using the variable ${DYNAMICTESTS} (plural).
This variable must be a string and the list of names must be pipe-seperated (``|``).

Example:

.. code::

    robot --variable DYNAMICTESTS:firstsuitename.testcase1|firstsuitename.testcase3|anothersuitename.othertestcase foldername

It is also possible to set the variable @{DYNAMICTESTS} as a list variable from i.e. python code.


Re-run failed test cases:
~~~~~~~~~~~~~~~~~~~~~~~~~

Because it is not possible to use the command line argument ``--rerunfailed`` from robot directly,
DataDriver brings a Pre-Run-Modifier that handles this issue.

Normally reexecution of failed testcases has three steps.

- original execution
- re-execution the failed ones based on original execution output
- merging original execution output with re-execution output

The DataDriver.rerunfailed Pre-Run-Modifier removes all passed test cases based on a former output.xml.

Example:

.. code ::

    robot --output original.xml tests                                                    # first execute all tests
    robot --prerunmodifier DataDriver.rerunfailed:original.xml --output rerun.xml tests  # then re-execute failing
    rebot --merge original.xml rerun.xml                                                 # finally merge results


Be aware, that in this case it is not allowed to use "``:``" as character in the original output file path.
If you want to set a full path on windows like ``e:\\myrobottest\\output.xml`` you have to use "``;``"
as argument seperator.

Example:

.. code ::

    robot --prerunmodifier DataDriver.rerunfailed;e:\\myrobottest\\output.xml --output e:\\myrobottest\\rerun.xml tests



Filtering with tags.
~~~~~~~~~~~~~~~~~~~~

New in ``0.3.1``

It is possible to use tags to filter the data source.
To use this, tags must be assigned to the test cases in data source.


Robot Framework® Command Line Arguments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To filter the source, the normal command line arguments of Robot Framework® can be used.
See Robot Framework® Userguide_ for more information
Be aware that the filtering of Robot Framework® itself is done before DataDriver is called.
This means if the Template test is already filtered out by Robot Framework®, DataDriver can never be called.
If you want to use ``--include`` the DataDriver TestSuite should have a ``DefaultTag`` or ``ForceTag`` that
fulfills these requirements.

.. _Userguide: http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#tag-patterns

Example: ``robot --include 1OR2 --exclude foo DataDriven.robot``


Filter based on Library Options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is also possible to filter the data source by an init option of DataDriver.
If these Options are set, Robot Framework® Filtering will be ignored.

Example:

.. code :: robotframework

    *** Settings ***
    Library    DataDriver    include=1OR2    exclude=foo




Configure DataDriver by Pre-Run Keyword
---------------------------------------

With ``config_keyword=`` it's possible to name a keyword that will be called from Data Driver before it starts the actual processing of the ``data file``.
One possible usage is if the ``data file`` itself shall be created by another keyword dynamically during the execution of the Data Driver test suite.
The ``config_keyword=`` can be used to call that keyword and return the updated arguments (e.g. ``file``) back to the Data Driver Library.

The ``config keyword``

- May be defined globally or inside each testsuite individually
- Gets all the arguments, that Data Driver gets from Library import, as a Robot Dictionary
- Shall return the (updated) Data Driver arguments as a Robot Dictionary

Usage in Robot Framework®

.. code :: robotframework

    *** Settings ***
    Library           OperatingSystem
    Library           DataDriver    dialect=excel    encoding=utf_8   config_keyword=Config
    Test Template     The Keyword

    *** Test Cases ***
    Test    aaa

    *** Keywords ***
    The Keyword
        [Arguments]    ${var}
        Log To Console    ${var}

    Config
        [Arguments]    ${original_config}
        Log To Console    ${original_config.dialect}                # just a log of the original
        Create File    ${CURDIR}/test321.csv
        ...    *** Test Cases ***,\\${var},\\n123,111,\\n321,222,      # generating file
        ${new_config}=    Create Dictionary    file=test321.csv     # set file attribute in a dictionary
        [Return]    ${new_config}                                   # returns {'file': 'test321.csv'}



Pabot and DataDriver
--------------------

You should use Pabot version 1.10.0 or newer.

DataDriver supports ``--testlevelsplit`` from pabot only if the PabotLib is in use.
Use ``--pabotlib`` to enable that.

When using pabot like this, DataDriver automatically splits the amount of test cases into nearly same sized groups.
Is uses the processes count from pabot to calculate the groups.
When using 8 processes with 100 test cases you will get 8 groups of tests with the size of 12 to 13 tests.
These 8 groups are then executed as one block with 8 processes.
This reduces a lot of overhead with Suite Setup and Teardown.

You can switch between three modes:

- ``Equal``: means it creates equal sizes groups
- ``Binary``: is more complex. it created a decreasing size of containers to support better balancing.
- ``Atomic``: it does not group tests at all and runs really each test case in a separate thread.

This can be set by ``optimize_pabot`` in Library import.


**Example**:

.. code :: robotframework

    *** Settings ***
    Library          DataDriver    optimize_pabot=Binary

Binary creates with 40 test cases and 8 threads something like that:

.. code ::

    P01: 01,02,03,04,05
    P02: 06,07,08,09,10
    P03: 11,12,13,14,15
    P04: 16,17,18,19,20
    P05: 21,22,23
    P06: 24,25,26
    P07: 27,28,29
    P08: 30,31,32
    P09: 33
    P10: 34
    P11: 35
    P12: 36
    P13: 37
    P14: 38
    P15: 39
    P16: 40