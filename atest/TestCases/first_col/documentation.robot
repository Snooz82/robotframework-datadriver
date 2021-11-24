*** Settings ***
Library           DataDriver    encoding=UTF8
Test Template     Check


*** Test Cases ***
Documentation should be ${expected}


*** Keywords ***
Check
    [Arguments]    ${expected}
    log variables
    Should Be Equal    ${TEST DOCUMENTATION}    ${expected}
