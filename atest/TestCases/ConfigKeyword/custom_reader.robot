*** Settings ***
Library    Collections
Library    DataDriver    config_keyword=Config Reader
Test Template    check vars
Test Setup    Log  Hi i am a Setup
Test Teardown    Log    I am a Teardown


*** Test Cases ***
test default    1    2


*** Keywords ***
check vars
    [Arguments]    ${var_1}    ${var_2}
    Should Be Equal    ${var_1}    ${var_2}

Config Reader
    [Arguments]    ${config}
    ${new_config}=    Create Dictionary    reader_class=TestCases/custom_reader/custom_reader.py    min=0    max=8
    [Return]    ${new_config}