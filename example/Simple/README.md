# Simple use case with tag filtering
Because it is often desirable to run just a subset of tests, it can be necessary to use the filtering characteristic of test tags.

The built-in `robot` command arguments `--include` and `--exclude` cannot be used for this purpose because they build the list of test cases to be executed prior to loading any libraries such as DataDriver.  Even the `--prerunmodifier` does not precede the build list, so the best approach is to avoid the use of the built-in filtering.

Fortunately it is very straightforward to implement a simple filter for tags specified in the data by including one or more `--variable` arguments.  Each time the `includeTag` variable is set on the command line, the value will be used to apply a filter so that only rows with a tag in the `includeTag` filters will be executed.

## Example:
This illustrates how to use the tag filter feature with a single tag.

### Data file:
|*** Test Cases ***|${message}|[Documentation]|[Tags]|
|----|----|----|---|
|First test|Simple message with no tags|If there are some tags specified, this should not be executed||
|Second test|With the tag we want|Should be executed|lightweight|
|Third test|Without a tag we want|Should not be executed|detailed|
|Fourth test|Includes a tag we want, and others|Should be executed because the tag is included in the list|detailed,lightweight,more,and more|

### Robot spec:
```robot
*** Settings ***
Documentation
...  Simply filter the tags from the command line:
...  robot --variable includeTag:lightweight FilterCases.robot
Library  ${CURDIR}/../../src/DataDriver  Simple.csv  dialect=unix
Test Template  Logger

*** Test Cases ***
Run  Default Message

*** Keywords ***
Logger
    [Arguments]     ${message}
    Log To Console  ${message}
    Log To Console  ${TEST_TAGS}
```

### Command line:
`robot --variable includeTag:lightweight FilterCases.robot`

### Output:
```
==============================================================================
FilterCases :: Simply filter the tags from the command line: robot --variab...
==============================================================================
Second test :: Should be executed                                     With the tag we want
['lightweight']
Second test :: Should be executed                                     | PASS |
------------------------------------------------------------------------------
Fourth test :: Should be executed because the tag is included in t... Includes a tag we want, and others
['and more', 'detailed', 'lightweight', 'more']
Fourth test :: Should be executed because the tag is included in t... | PASS |
------------------------------------------------------------------------------
FilterCases :: Simply filter the tags from the command line: robot... | PASS |
2 critical tests, 2 passed, 0 failed
2 tests total, 2 passed, 0 failed
```
