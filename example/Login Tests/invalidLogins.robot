*** Settings ***
Resource    login_resources.robot
Suite Setup    Open my Browser
Suite Teardown    Close Browsers    
Test Setup      Open Login Page
Test Template    Invalid login


*** Test Cases ***       Benutzer       Passwort
Right user empty pass    demo    ${EMPTY}    [Tags]
Right user wrong pass    demo    FooBar 
    
Empty user right pass    ${EMPTY}       mode
Empty user empty pass    ${EMPTY}       ${EMPTY}
Empty user wrong pass    ${EMPTY}       FooBar 
    
Wrong user right pass    FooBar       mode
Wrong user empty pass    FooBar       ${EMPTY}
Wrong user wrong pass    FooBar       FooBar 
        
*** Keywords ***
Invalid login
    [Arguments]    ${username}    ${password}
    Input username    ${USERNAME} 
    Input pwd    ${PASSWORD} 
    click login button
    Error page should be visible