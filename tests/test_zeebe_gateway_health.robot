*** Settings ***
Documentation       This test suite contains test cases for Zeebe gateway Health
...                 check.

Library             ../libraries/zeebe/GatewayLibrary.py    ${ZEEBE_GATEWAY_HOST}


*** Variables ***
${ZEEBE_GATEWAY_HOST}       localhost


*** Test Cases ***
Zeebe gateway status should be healthy
    [Documentation]    Pools the Zeebe gateway until it is healthy.
    Wait Until Keyword Succeeds    30    1s
    ...    Check Gateway Status Is Healthy


*** Keywords ***
Check Gateway Status Is Healthy
    [Documentation]    This keyword checks if the Zeebe gateway is healthy.
    ${response}=    Get Gateway Health
    Should Be Equal As Strings    ${response.status_code}    200
    Should Be Equal As Strings    ${response.json()['status']}    UP
