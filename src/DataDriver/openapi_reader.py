# Copyright 2021-  Robin Mackaij
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

from pathlib import Path
from typing import Any, Dict, List

from .AbstractReaderClass import AbstractReaderClass
from .ReaderConfig import TestCaseData

try:
    import jsonref
    import ruamel.yaml
except ImportError:
    raise ImportError(
        """Requirements (jsonref) for OpenAPi support are not installed.
    Use 'pip install -U robotframework-datadriver[openapi]' to install OpenAPI support."""
    )

class openapi_reader(AbstractReaderClass):
    def get_data_from_source(self):
        test_data: List[TestCaseData] = []

        #TODO: add proper handling for loading errors
        file = Path(self.file)
        if file.suffix == ".yaml":
            yaml = ruamel.yaml.YAML(typ='safe')
            data = yaml.load(file)
            json_object = json.dumps(data, indent = 4)
            self.openapi_doc: Dict[str, Any] = jsonref.loads(json_object)
        else:
            self.openapi_doc: Dict[str, Any] = jsonref.load(file)
        try:
            endpoints: Dict[str, Any] = self.openapi_doc.get("paths")
        except KeyError:
            raise ValueError(f"{self.file} is not a valid OpenAPI document")
        for endpoint, methods in endpoints.items():
            for method, method_data in methods.items():
                for response in method_data.get("responses"):
                    # default applies to all status codes that are not specified like
                    # 401 and 403. These must be tested using another approach.
                    if response != "default":
                        #TODO: make tags configurable
                        tag_list: List[str] = []
                        if tags := method_data.get("tags", None):
                            tag_list.extend(tags)
                        tag_list.append(f"Method: {method.upper()}")
                        tag_list.append(f"Response: {response}")
                        test_data.append(
                            TestCaseData(
                                arguments={
                                    "${endpoint}": endpoint,
                                    "${method}": method.upper(),
                                    "${status_code}": response,
                                },
                                tags=tag_list
                            )
                        )
        return test_data
