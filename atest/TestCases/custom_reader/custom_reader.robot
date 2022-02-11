*** Settings ***
Library    DataDriver    reader_class=TestCases/custom_reader/custom_reader.py    optimize_pabot=equal
...            min=0    max=103
Test Template    check vars


*** Test Cases ***
test default    1    2


*** Keywords ***
check vars
    [Arguments]    ${var_1}    ${var_2}
    Should Be Equal    ${var_1}    ${var_2}