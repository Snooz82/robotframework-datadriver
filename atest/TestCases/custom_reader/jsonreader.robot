*** Settings ***
Library    DataDriver    data.json
Test Template    log vars


*** Test Cases ***
test default    1    2


*** Keywords ***
log vars
    [Arguments]    ${username}    ${password}
    Log To Console    \${username}: ${username}
    Log To Console    \${password}: ${password}