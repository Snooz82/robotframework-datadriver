*** Settings ***
Library           SeleniumLibrary

*** Variables ***
${LOGIN URL}      http://localhost:7272
${BROWSER}        firefox

*** Keywords ***
Open my Browser
    Open Browser    ${LOGIN URL}    browser=${BROWSER}
    Set Window Position    0    0
    Set Window Size    960    1000

Close Browsers
    Close All Browsers

Open Login Page
    Go To    ${LOGIN URL}

Input username
    [Arguments]    ${username}
    Input Text    id=username_field    ${username}

Input pwd
    [Arguments]    ${password}
    Input Password    id=password_field    ${password}

click login button
    Click Button    id=login_button

welcome page should be visible
    Title Should Be    Welcome Page

Error page should be visible
    Title Should Be    Error Page
