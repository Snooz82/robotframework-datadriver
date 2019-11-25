# Copyright 2018-  René Rohner
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from DataDriver.AbstractReaderClass import AbstractReaderClass  # inherit class from AbstractReaderClass
from DataDriver.ReaderConfig import TestCaseData  # return list of TestCaseData to DataDriver


class custom_reader(AbstractReaderClass):

    def get_data_from_source(self):  # This method will be called from DataDriver to get the TestCaseData list.
        test_data = []
        for i in range(int(self.kwargs['min']), int(self.kwargs['max'])):  # Dummy code to just generate some data
            args = {'${var_1}': str(i), '${var_2}': str(i)}  # args is a dictionary. Variable name is the key, value is value.
            test_data.append(TestCaseData(f'test {i}', args, ['tag']))  # add a TestCaseData object to the list of tests.
        return test_data  # return the list of TestCaseData to DataDriver
