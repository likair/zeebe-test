*** Settings ***
Documentation       This test suite contains test cases for Zeebe process.

Library             ../libraries/zeebe/ZbctlLibrary.py    ${ZEEBE_GATEWAY_HOST}    insecure=True


*** Variables ***
${ZEEBE_GATEWAY_HOST}       localhost
${EMPTY_PROCESS}            ${CURDIR}/../resources/data/empty_process.xml
${ADVANCED_PROCESS}         ${CURDIR}/../resources/data/advanced_process.xml


*** Test Cases ***
Deploy an empty process and create a process instance
    [Tags]    smoke    process
    [Documentation]    Checks an empty process can be deployed and a process
    ...    instance can be created.
    ${response}=    GIVEN Deploy Resource    ${EMPTY_PROCESS}
    ${response}=    WHEN Create Process Instance
    ...    ${response['deployments'][0]['process']['bpmnProcessId']}
    THEN Should Be Equal As Strings    ${response['variables']}    {}

Create a process instance with non-existing process
    [Tags]    smoke    process    negative
    [Documentation]    Checks a process instance cannot be created with a non-
    ...    existing process.
    ${response}=    GIVEN Create Process Instance    non-existing-process
    THEN Should Contain    ${response}    NOT_FOUND

Deploy an advanced process and create a process instance
    [Tags]    process
    [Documentation]    Checks an advanced process can be deployed and a process
    ...    instance can be created, if a worker is available.
    ${response_1}=    GIVEN Deploy Resource    ${ADVANCED_PROCESS}
    ${response_2}=    WHEN Create Worker
    ...    test-worker
    ...    "echo {\\"result\\":\\"Pong\\"}"
    ${response_2}=    AND Create Process Instance
    ...    ${response_1['deployments'][0]['process']['bpmnProcessId']}
    Then Should Be Equal As Strings
    ...    ${response_2['variables']}
    ...    {"result":"Pong"}

    [Teardown]    Terminate Workers

Deploy an advanced process and create a process instance without a worker
    [Tags]    process    negative    slow
    [Documentation]    Checks an advanced process can be deployed and a process
    ...    instance fails given no worker is available
    ${response}=    GIVEN Deploy Resource    ${ADVANCED_PROCESS}
    ${response}=    WHEN Create Process Instance
    ...    ${response['deployments'][0]['process']['bpmnProcessId']}
    THEN Should Contain    ${response}    DeadlineExceeded
