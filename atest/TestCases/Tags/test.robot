*** Settings ***
Library           DataDriver    reader_class=foo_reader.py     handle_template_tags=DefaultTags
Test Template     Foo Template
Force Tags        default


*** Test Cases ***
Execute Toolchain for ${fooarg}


*** Keywords ***
Foo Template
    [Arguments]    ${fooarg}
    Log To Console   ${fooarg} - Tags: ${TEST TAGS}