*** Settings ***
Library           DataDriver    encoding=UTF8
Test Template     Check


*** Test Cases ***
Tags should containe ${expected}


*** Keywords ***
Check
    [Arguments]    ${expected}
    Should Be Equal    ${TEST TAGS}[0]    ${expected}
