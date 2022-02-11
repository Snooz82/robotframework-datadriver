### Environment

To test DataDriver i would strongly recomment to create virtual environment.

Steps:
- First fork DataDriver
- Clone the fork to you disk
- in your terminal execute `python -m venv .venv` in the main folder of robotframework-datadriver
- activate that virtual environment (unix: `source .venv/bin/activate`)
- install all requirements `pip install -r dev-requirements.txt`
- install DataDriver editable from source `pip install -e .`

### ATests

To run the acceptance tests, navigate to the `atest` folder and execute the `run_atest.sh` or `run_atest.bat`.
There shall be 700 passed test cases. Lower or different numbers are failures.

#### Pabot tests

To run pabot tests, just run `run_atest_pabot.sh` .
697 test cases shall pass. 3 are filtered and not executable with pabot.
These test will take much longer than not parallel, due to the heavy overhead of Robot starting.

