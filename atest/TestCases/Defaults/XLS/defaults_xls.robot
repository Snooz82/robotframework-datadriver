*** Settings ***
Library    DataDriver    defaults_xls.xls
Test Template    Check Variables


*** Variables ***
${Default_Tags}=    []

*** Test Cases ***            ${var_1}    ${var_2}    ${var_name}   ${var_doc}                           ${var_tags}
default ${var_1} ${var_2}     a           a           defaults      This is the Default Documentation    ${Default_Tags}
    [Documentation]    This is the Default Documentation

*** Keywords ***
Check Variables
    [Arguments]    ${var_1}    ${var_2}    ${var_name}   ${var_doc}   ${var_tags}
    Verify Variable    ${var_1}                 ${var_2}          a
    Verify Variable    ${TEST_DOCUMENTATION}    ${var_doc}        This is the Default Documentation
    Verify Variable    ${TEST_NAME}             ${var_name}       defaults
    Verify Variable    ${TEST_TAGS}             ${var_tags}       ${Default_Tags}


Verify Variable
    [Arguments]    ${var}    ${exp_var}    ${default}
    Run Keyword And Continue On Failure   Should Not Be Equal    ${var}    ${default}
    Run Keyword And Continue On Failure   Should Be Equal As Strings    ${var}    ${exp_var}    
        