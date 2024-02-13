*** Settings ***
Library             DataDriver    encoding=utf8

Suite Setup         Suite Start
Suite Teardown      Suite End
Test Setup          Start
Test Teardown       End
Test Template       DataDriver demo

Force Tags          nopabot


*** Test Cases ***
Datadriver execution: ${number}


*** Keywords ***
Suite Start
    Set Suite Variable    ${idx}    ${1}
    Log    Suite Setup ${idx}
    Log    ${{json.dumps($DataDriver_DATA_LIST, indent=2)}}
    Log    ${{json.dumps($DataDriver_DATA_DICT, indent=2)}}

Start
    Set Suite Variable    ${idx}    ${idx+1}
    Log    \nTask Setup ${idx}
    Log    ${{json.dumps($DataDriver_TEST_DATA, indent=2)}}

DataDriver demo
    [Arguments]    ${number}
    Set Suite Variable    ${idx}    ${idx+1}
    Log    Task Execution ${idx}
    Should Be Equal    ${idx}    ${number}

End
    Set Suite Variable    ${idx}    ${idx+1}
    Log    Task Teardown ${idx}

Suite End
    Set Suite Variable    ${idx}    ${idx+1}
    Log    Suite Teardown ${idx}
    Should Be Equal    ${idx}    ${11}
