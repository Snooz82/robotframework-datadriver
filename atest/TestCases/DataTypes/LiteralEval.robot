*** Settings ***
Test Template    TestKeyword
Library          DataDriver    encoding=utf-8


*** Test Cases ***
Template Test

*** Keywords ***
TestKeyword
    [Arguments]    ${scalar}    ${dict}    ${list}    ${dotdict}    ${user}
    Log     ${scalar}
    Log     ${dict}
    Log     ${dict}[name]
    Log     ${list}
    Log     ${dotdict.key}
    Log     ${dotdict}[key2]
    Log     ${user}
    Log     ${user}[name][first]
    Log     ${user.name.last}
    Log     ${user.nr}
    Log     ${user.dict}[test]
    Log     ${user}[pwd]
    Log Many    ${scalar}
    Log Many    &{dict}
    Log Many    @{list}
    Log Many    &{dotdict}