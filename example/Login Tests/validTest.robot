*** Settings ***    
Resource    login_resources.robot

*** Test Cases ***
valid Login
    [Setup]    Open my Browser
    Input username    demo
    Input pwd    mode
    click login button
    welcome page should be visible
    [Teardown]    Close Browsers 