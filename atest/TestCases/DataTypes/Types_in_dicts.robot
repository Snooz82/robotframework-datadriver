*** Settings ***
Test Template     TestKeyword
Library           DataDriver    encoding=utf_8

*** Test Cases ***
Template Test


*** Keywords ***
TestKeyword
    [Arguments]    ${dict}    ${exp}
    Should Be Equal    ${dict}    ${exp}
    Log To Console    \n${dict}
