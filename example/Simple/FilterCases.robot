*** Settings ***
Documentation
...  Simply filter the tags from the command line:
...  robot --variable includeTags:lightweight FilterCases.robot

Library  ${CURDIR}/../../src/DataDriver  Simple.csv  dialect=unix   include_tags=${includeTags}

Test Template  Logger

*** Test Cases ***
Run  Default Message

*** Keywords ***
Logger
    [Arguments]     ${message}
    Log To Console  ${message}
    Log To Console  ${TEST_TAGS}
