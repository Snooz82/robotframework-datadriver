*** Settings ***
Library             DataDriver    encoding=UTF8

Test Template       Check

Force Tags          failing


*** Test Cases ***
Template    1    0


*** Keywords ***
Check
    [Arguments]    ${value}    ${expected}
    Should Be Equal    ${value}    ${expected}
