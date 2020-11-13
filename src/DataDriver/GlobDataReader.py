"""This module implements a robotframework-datadriver DataReader to turn a glob pattern of files into a csv interface

Example .robot file template:

*** Settings ***
Library         DataDriver  file=/path/to/my/files/**.json  reader_class=DataDriver.GlobDataReader  file_search_strategy=None  var_name=\${file_name}
Test Template   My Test Template

*** Test Cases ***

DataDriver Test  NO_FILE

*** Keywords ***

My Test Template
    [Arguments]  ${file_name}
    My Test Keyword  ${file_name}


"""

import os
import glob

from DataDriver.AbstractReaderClass import AbstractReaderClass
from DataDriver.ReaderConfig import TestCaseData

class GlobDataReader(AbstractReaderClass):

    def __init__(self, reader_config):
        super().__init__(reader_config)

    def get_data_from_source(self):
        """Returns a list of TestCaseData to DataDriver"""
        self._read_glob_to_data_table()
        return self.data_table

    def _read_glob_to_data_table(self):
        var_name = self.kwargs["var_name"] if "var_name" in self.kwargs else "${file_name}"
        self._analyse_header(["*** Test Cases ***", var_name])
        for f in glob.glob(self.file):
            tcName = os.path.basename(os.path.splitext(f)[0])
            p = os.path.abspath(f).replace("\\","/") 
            self._read_data_from_table([tcName,p])
