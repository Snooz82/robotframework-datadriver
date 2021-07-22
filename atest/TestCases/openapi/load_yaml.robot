*** Settings ***
Library            DataDriver    reader_class=openapi_reader
...                    file=${root}/atest/TestCases/openapi/petstore_openapi.yaml
# Force Tags         OpenAPI
Suite Setup        Validate OpenAPI specification
Test Template      Do Nothing


*** Test Cases ***
Some OpenAPI test for ${method} on ${endpoint} where ${status_code} is expected

*** Keywords *** ***
Do Nothing
    [Arguments]    ${endpoint}    ${method}    ${status_code}
    No Operation

Validate OpenAPI specification
    [Documentation]
    ...    Validate the retrieved document against the OpenApi 3.0 specification
    Validate OpenAPI Document
