*** Settings ***
Documentation    Validate that file is handed if both reader_class and file are
...              specified
Library    DataDriver    reader_class=TestCases/custom_reader/custom_reader.py
...            min=0    max=3    file=dummy.txt
Test Template    check vars


*** Test Cases ***
test default    1    2


*** Keywords ***
check vars
    [Arguments]    ${var_1}    ${var_2}
    Should Be Equal    ${var_1}    ${var_2}