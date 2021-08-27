*** Settings ***
Library    DataDriver    defaults_xlsx.xlsx     sheet_name=DataTypes    preserve_xls_types=True
Test Template    Check Variables


*** Variables ***
${Default_Tags}=    []

*** Test Cases ***                                    ${var_1}    ${var_2}    ${var_name}   ${var_doc}                           ${var_tags}
Test: ${var_1} isinstance ${var_2} (${var_name})      a           a           a             This is the Default Documentation    ${Default_Tags}
    [Documentation]    This is the Default Documentation

*** Keywords ***
Check Variables
    [Arguments]    ${var_1}    ${var_2}     ${var_name}
    Log      ${{type($var_1)}} == ${var_2} => ${{str(type($var_1)) == $var_2}}
    Verify Variable     ${{type($var_1)}}    ${var_2}     ${var_name}


Verify Variable
    [Arguments]    ${var}    ${exp_var}    ${default}
    Run Keyword And Continue On Failure   Should Not Be Equal As Strings    ${var}    ${default}
    Run Keyword And Continue On Failure   Should Be Equal As Strings    ${var}    ${exp_var}
