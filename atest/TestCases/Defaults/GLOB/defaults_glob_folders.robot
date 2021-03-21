*** Settings ***
Library           DataDriver    file=${CURDIR}/FoldersToFind/*/    reader_class=glob_reader
Library           OperatingSystem
Test Template     Test all Files

*** Test Cases ***
Glob_Reader_Test
    Wrong_File.NoJson

*** Keywords ***
Test all Files
    [Arguments]    ${file_name}
    ${content}=    Get File    ${file_name}/verify.txt
    Should Be Equal    ${TEST_NAME}    ${content}
