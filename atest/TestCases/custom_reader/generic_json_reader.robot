*** Settings ***
Library    DataDriver    file=data.json   reader_class=generic_json_reader
Test Template    log vars

Test Tags    json


*** Test Cases ***
${test_case_name}   1    2


*** Keywords ***
log vars
    [Arguments]    ${arguments}    ${tags}
    Should Not Be Empty    ${tags}    Failed to load tags from test case data.
    Set Tags    @{tags}
    Should Not Be Empty    ${arguments}    Failed to load arguments from test case data.
    Log To Console    \${argumentes}: ${arguments}
    Log To Console    username: ${arguments}[\${username}]
    Log To Console    password: ${arguments}[\${password}]