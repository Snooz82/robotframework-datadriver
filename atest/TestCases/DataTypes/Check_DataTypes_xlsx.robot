*** Settings ***
Library    DataDriver    file=.xlsx    encoding=utf-8
Library    Collections
Test Template   Test

*** Test Cases ***
Tempalte

*** Keywords ***
Test
    [Arguments]    ${scalar}     ${list}    ${list_eval}    ${dict}    ${dict_eval}     ${eval}     ${exp_eval}    ${user}
    Run Keyword    ${scalar}    ${eval}    ${exp_eval}
    Lists Should Be Equal   ${list}   ${list_eval}
    FOR    ${Key}   IN   @{dict_eval}
        Should Be Equal    ${dict.${Key}}    ${dict_eval}[${Key}]
    END
    Validate User    ${user}



Sum List
    [Arguments]    ${inputs}    ${expected}
    ${sum}=    Set Variable    ${0}
    FOR    ${item}    IN    @{inputs}
        ${sum}=    Evaluate    int($item) + int($sum)
    END
    Should Be Equal As Integers    ${sum}    ${expected}

Whos Your Daddy
    [Arguments]    ${input}    ${expected}
    Should Be Equal    ${input}[Daddy]    ${expected}

Validate User
    [Arguments]    ${user}
    Should Be Equal    ${user}[id]            ${user}[chk][id]
    Should Be Equal    ${user.name.first}     ${user}[chk][first]
    Should Be Equal    ${user}[name][last]    ${user}[chk][last]
    