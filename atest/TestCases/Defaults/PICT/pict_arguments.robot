*** Settings ***
Library    DataDriver    pict_arg.pict    pict_options=/o:3
Library    Collections
Test Template    Check Variables


*** Variables ***
@{COMBO}=

*** Test Cases ***            ${var_1}    ${var_2}
${Type}_${Size}_${Format method}_${File system}_${Cluster size}_${Compression}

*** Keywords ***
Check Variables
    [Arguments]    ${Type}    ${Size}    ${Format method}    ${File system}    ${Cluster size}    ${Compression}
    ${comb}=    Set Variable    ${Type} ${Size} ${Format method} ${File system} ${Cluster size} ${Compression}
    IF  $comb in $COMBO
        Fail    "${comb}" is doubled...
    END
    Append To List    ${COMBO}    ${comb}
