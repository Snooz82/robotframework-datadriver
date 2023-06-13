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
from .xlsx_reader import nan, pd, xlsx_reader


class xls_reader(xlsx_reader):
    def read_data_frame_from_file(self, dtype):
        return pd.read_excel(self.file, sheet_name=self.sheet_name, dtype=dtype).replace(
            nan, "", regex=True
        )
