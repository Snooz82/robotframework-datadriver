*** Settings ***
Library          DataDriver    file=10000.csv    reader_class=generic_csv_reader
Test Template    Check Variables
Force Tags       performance


*** Variables ***
${Default_Tags}=    []

*** Test Cases ***            ${var_1}    ${var_2}    ${var_name}
test ${var_1}|${var_2}     a           a           defaults

*** Keywords ***
Check Variables
    [Arguments]    ${var_1}    ${var_2}    ${var_name} 
    Verify Variable    ${var_1}                 ${var_2}          a
    Verify Variable    ${TEST_NAME}             ${var_name}       default a a


Verify Variable
    [Arguments]    ${var}    ${exp_var}    ${default}
    Run Keyword And Continue On Failure   Should Not Be Equal    ${var}    ${default}
    Run Keyword And Continue On Failure   Should Be Equal As Strings    ${var}    ${exp_var}    
        