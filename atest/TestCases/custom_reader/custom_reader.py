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


from DataDriver.AbstractReaderClass import AbstractReaderClass
from DataDriver.ReaderConfig import TestCaseData


class custom_reader(AbstractReaderClass):

    def get_data_from_source(self):
        print(self.kwargs)
        test_data = []
        for i in range(int(self.kwargs['min']), int(self.kwargs['max'])):
            args = {'${var_1}': str(i), '${var_2}': str(i)}
            test_data.append(TestCaseData(f'test {i}', args, ['tag']))
        return test_data
