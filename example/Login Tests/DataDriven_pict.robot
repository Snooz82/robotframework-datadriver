*** Settings ***
Library             DataDriver    DataDriven.pict
Resource            login_resources.robot

Suite Setup         Open my Browser
Suite Teardown      Close Browsers
Test Setup          Open Login Page
Test Template       Invalid Login


*** Test Cases ***
Login with user '${username}' and password '${password}'    Default    UserData


*** Keywords ***
Invalid login
    [Tags]    flat
    [Arguments]    ${username}    ${password}
    Input username    ${username}
    Input pwd    ${password}
    click login button
    Error page should be visible
