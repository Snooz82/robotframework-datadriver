*** Settings ***
Library           DataDriver
Resource          login_resources.robot

Suite Setup       Get Vars   # Open my Browser
Test Setup        Open Login Page
Test Template     Invalid Login
Suite Teardown    Close Browsers

*** Test Cases ***
Login with user '${username}' and password '${password}'    Default    UserData

*** Keywords ***
Invalid login
    [Arguments]    ${username}   ${password}
    Input username    ${username}
    Input pwd    ${password}
    click login button
    Error page should be visible

Get Vars
    Log Many    @{DataDriver_DATA_LIST}
    Log Many    &{DataDriver_DATA_DICT}
    Log To Console    ${{json.dumps($DataDriver_DATA_LIST, indent=2)}}
    Log To Console    ${{json.dumps($DataDriver_DATA_DICT, indent=2)}}