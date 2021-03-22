*** Settings ***
Library           DataDriver    file=${CURDIR}/DataFiles/*_File.json    reader_class=glob_reader
Library           OperatingSystem
Test Template     Test all Files


*** Test Cases ***
Glob_Reader_Test    Wrong_File.NoJson


*** Keywords ***
Test all Files
    [Arguments]    ${file_name}
    ${file_content}=    Get File    ${file_name}
    ${content}=    Evaluate    json.loads($file_content)["test_case"]
    Should Be Equal    ${TEST_NAME}    ${content}