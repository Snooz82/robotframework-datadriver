*** Settings ***
Library             DataDriver    encoding=utf_8

Test Template       TestKeyword

Test Tags           rf7only


*** Test Cases ***
Template Test


*** Keywords ***
TestKeyword
    [Arguments]    ${opt}=default    ${exp}=Wrong    ${dict}=Value  
    Should Be Equal    ${dict}    ${exp}
    Log To Console    \n${dict}
    Should Be Equal    ${opt}    default
