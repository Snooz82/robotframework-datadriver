*** Settings ***
Library    DataDriver    reader_class=./custom_reader.py
...            min=0    max=16
Test Template    check vars


*** Test Cases ***
test default    1    2


*** Keywords ***
check vars
    [Arguments]    ${var_1}    ${var_2}
    Should Be Equal    ${var_1}    ${var_2}