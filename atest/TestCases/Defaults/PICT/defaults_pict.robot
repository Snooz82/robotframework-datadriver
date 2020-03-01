*** Settings ***
Library    DataDriver    .pict
Test Template    Check Variables


*** Variables ***
${Default_Tags}=    []

*** Test Cases ***            ${var_1}    ${var_2}
default ${var_1} ${var_2}     a           a       

*** Keywords ***
Check Variables
    [Arguments]    ${var_1}    ${var_2}
    Should Not Be Equal As Strings    ${var_1}    ${var_2}        
    