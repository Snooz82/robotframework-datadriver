*** Settings ***
Library    DataDriver    reader_class=TestCases/custom_reader/custom_reader.py    min=0    file_search_strategy=None    max=62
Test Template    check vars


*** Test Cases ***
test default    1    2


*** Keywords ***
check vars
    [Arguments]    ${var_1}    ${var_2}
    Should Be Equal    ${var_1}    ${var_2}