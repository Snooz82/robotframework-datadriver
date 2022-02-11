*** Settings ***
Library           OperatingSystem
Library           DataDriver    dialect=excel    encoding=utf_8   config_keyword=Config
Suite Setup       Suite Setup Keyword
Test Template     The Test Keyword
Suite Teardown    Remove File    ${CURDIR}/${random}test321.csv

*** Test Cases ***
Test    aaa

*** Keywords ***
Suite Setup Keyword
    Log   This is the single Suite Setup

The Test Keyword
    [Arguments]    ${var}
    Log To Console    ${var}

Config
    [Arguments]    ${original_config}
    Log To Console    ${original_config.dialect}
    Set Global Variable    ${random}    ${{random.randint(0,1000)}}
    Create File    ${CURDIR}/${random}test321.csv
    ...    *** Test Cases ***,\${var},\nTestCase1,111,\nTestCase2,222,
    ${new_config}=    Create Dictionary    file=${random}test321.csv
    [Return]    ${new_config}
