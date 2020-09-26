*** Settings ***
Library           OperatingSystem
Library           DataDriver    dialect=excel    encoding=utf_8   config_keyword=Config
Test Template     The Test Keyword
Suite Teardown    Remove File    ${CURDIR}/test321.csv

*** Test Cases ***
Test    aaa

*** Keywords ***
The Test Keyword
    [Arguments]    ${var}
    Log To Console    ${var}

Config
    [Arguments]    ${original_config}
    Log To Console    ${original_config.dialect}
    Remove File    ${CURDIR}/test321.csv
    File Should Not Exist    ${CURDIR}/test321.csv
    Create File    ${CURDIR}/test321.csv
    ...    *** Test Cases ***,\${var},\nTestCase1,111,\nTestCase2,222,
    ${new_config}=    Create Dictionary    file=test321.csv
    [Return]    ${new_config}
