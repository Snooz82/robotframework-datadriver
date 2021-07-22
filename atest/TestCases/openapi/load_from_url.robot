*** Settings ***
Library            DataDriver    reader_class=openapi_reader
...                    url=http://127.0.0.1:8000/openapi.json
...                    origin=http://127.0.0.1:8000
...                    base_path=${EMPTY}
Force Tags         OpenAPI
Suite Setup        Validate OpenAPI specification
Test Template      Validate Test Endpoint Keyword


*** Test Cases ***
Test Endpoint for ${method} on ${endpoint} where ${status_code} is expected

*** Keywords *** ***
Validate Test Endpoint Keyword
    [Arguments]    ${endpoint}    ${method}    ${status_code}
    Test Endpoint
    ...    endpoint=${endpoint}    method=${method}    status_code=${status_code}

Validate OpenAPI specification
    [Documentation]
    ...    Validate the retrieved document against the OpenApi 3.0 specification
    Validate OpenAPI Document
