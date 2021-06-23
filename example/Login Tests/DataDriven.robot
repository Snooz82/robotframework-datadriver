*** Settings ***
Library           DataDriver
Resource          login_resources.robot

Suite Setup       Open my Browser
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
