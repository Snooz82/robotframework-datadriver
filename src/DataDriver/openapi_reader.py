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

from logging import getLogger
from typing import Any, Dict, List

from DataDriver.AbstractReaderClass import AbstractReaderClass
from DataDriver.ReaderConfig import TestCaseData

try:
    from prance import ResolvingParser
    from prance.util.url import ResolutionError
except ImportError:
    raise ImportError(
        """Requirements (prance) for OpenAPi support is not installed.
    Use 'pip install -U robotframework-datadriver[openapi]' to install OpenAPI support."""
    )


logger = getLogger(__name__)


class OpenapiReader(AbstractReaderClass):
    def get_data_from_source(self) -> List[TestCaseData]:
        test_data: List[TestCaseData] = []

        try:
            if url := self.reader_config.kwargs.get("url", None):
                parser = ResolvingParser(url)
            else:
                parser = ResolvingParser(self.file)
        except ResolutionError as exception:
            BuiltIn().fatal_error(
                f"Exception while trying to load openapi spec from url: {exception}"
            )
        endpoints: Dict[str, Any] = parser.specification.get("paths")
        if ignored_endpoints := self.reader_config.kwargs.get("ignored_endpoints", None):
            for endpoint in ignored_endpoints:
                endpoints.pop(endpoint, None)
        ignored_responses = self.reader_config.kwargs.get("ignored_responses", [])
        ignore_fastapi_default_422 = self.reader_config.kwargs.get("ignore_fastapi_default_422", False)
        for endpoint, methods in endpoints.items():
            for method, method_data in methods.items():
                for response in method_data.get("responses"):
                    # FastAPI also adds a 422 response to endpoints that do not take
                    # parameters that can be invalidated. Since header-invalidation is
                    # currently not supported, these endpoints can be filtered by a
                    # generic flag
                    if response == "422" and method in ["get", "delete"] and ignore_fastapi_default_422:
                        continue
                    # default applies to all status codes that are not specified, in
                    # which case we don't know what to expect and thus can't verify
                    if response == "default" or response  in ignored_responses:
                        continue
                    tag_list: List[str] = []
                    if tags:= method_data.get("tags", None):
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


# Support Robot Framework import mechanism
openapi_reader = OpenapiReader    # pylint: disable=invalid-name
