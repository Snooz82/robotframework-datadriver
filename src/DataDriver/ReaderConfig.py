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

from typing import Optional, Any, Dict, List

from robot.utils import DotDict

from .utils import PabotOpt


class ReaderConfig:

    TEST_CASE_TABLE_NAME = "*** Test Cases ***"

    def __init__(
        self,
        file: Optional[str] = None,
        encoding: Optional[str] = None,
        dialect: Optional[str] = None,
        delimiter: Optional[str] = None,
        quotechar: Optional[str] = None,
        escapechar: Optional[str] = None,
        doublequote: Optional[bool] = None,
        skipinitialspace: Optional[bool] = None,
        lineterminator: Optional[str] = None,
        sheet_name: Any = None,
        reader_class: Optional[str] = None,
        file_search_strategy: str = "path",
        file_regex: Optional[str] = None,
        include: Optional[str] = None,
        exclude: Optional[str] = None,
        list_separator: Optional[str] = ",",
        config_keyword: Optional[str] = None,
        optimize_pabot: PabotOpt = PabotOpt.Equal,
        **kwargs
    ):

        self.file = file
        self.encoding = encoding
        self.dialect = dialect
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.escapechar = escapechar
        self.doublequote = doublequote
        self.skipinitialspace = skipinitialspace
        self.lineterminator = lineterminator
        self.sheet_name = sheet_name
        self.reader_class = reader_class
        self.file_search_strategy = file_search_strategy
        self.file_regex = file_regex
        self.include = include
        self.exclude = exclude
        self.list_separator = list_separator
        self.config_keyword = config_keyword
        self.optimize_pabot = optimize_pabot
        self.kwargs = kwargs


class TestCaseData(DotDict):
    def __init__(
        self,
        test_case_name: str = "",
        arguments: Optional[Dict] = None,
        tags: Optional[List] = None,
        documentation: str = "",
    ):
        super().__init__()
        self.test_case_name = test_case_name
        self.arguments = arguments if arguments else {}
        self.tags = tags
        self.documentation = documentation
