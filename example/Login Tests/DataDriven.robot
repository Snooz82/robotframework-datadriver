*** Settings ***
Library           DataDriver
Resource          login_resources.robot

Suite Setup       Open my Browser
Test Setup        Open Login Page
Test Template     Invalid Login
Suite Teardown    Close Browsers

Force Tags        1    2

*** Variables ***
${default}    name=Default    password=UserData

*** Test Cases ***
Login with user '${user.name}' and password '${user.password}'    ${default}

*** Keywords ***
Invalid login
    [Arguments]    ${user}
    [Tags]    FLAT
    Set Selenium Speed    500ms
    Input username    ${user.name}
    Input pwd    ${user.password}
    click login button
    Error page should be visible
