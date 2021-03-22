*** Settings ***
Library           DataDriver    file=${CURDIR}/FoldersToFind/*/    reader_class=glob_reader    arg_name=\${folder_name}
Library           OperatingSystem
Test Template     Test all Files


*** Test Cases ***
Glob_Reader_Test    Wrong_File.NoJson


*** Keywords ***
Test all Files
    [Arguments]    ${folder_name}
    ${content}=    Get File    ${folder_name}/verify.txt
    Should Be Equal    ${TEST_NAME}    ${content}
