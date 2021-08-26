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

#TODO: support ${itemId} mapping instead of only "id"

import json as _json
import sys
from dataclasses import asdict, make_dataclass
from importlib import import_module
from itertools import zip_longest
from logging import getLogger
from pathlib import Path
from random import choice, getrandbits, randint, uniform
from typing import Any, Dict, List, Optional, Tuple, Type, Union
from uuid import uuid4
from warnings import simplefilter

import jsonschema
from openapi_spec_validator import openapi_v3_spec_validator, validate_spec
from prance import ResolvingParser
from requests import Response, Session
from requests.auth import AuthBase, HTTPBasicAuth
from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn
from urllib3.exceptions import InsecureRequestWarning

from DataDriver.openapi.dto_base import (
    Dto,
    IdDependency,
    PropertyValueConstraint,
    UniquePropertyValueConstraint,
)


run_keyword = BuiltIn().run_keyword


logger = getLogger(__name__)
# Suppress certificate verification warning for self-signed certificate
simplefilter("ignore", category=InsecureRequestWarning)


@library(scope="GLOBAL")
class OpenapiExecutors:
    def __init__(
            self,
            source: str,
            origin: str = "",
            base_path: str = "",
            mappings_path: Union[str, Path] = "",
            username: str = "",
            password: str = "",
            auth: Optional[AuthBase] = None,
        ) -> None:
        parser = ResolvingParser(source)
        self.openapi_doc: Dict[str, Any] = parser.specification
        self.session = Session()
        self.origin = origin
        self.base_url = f"{self.origin}{base_path}"
        if auth:
            self.auth = auth
        else:
            self.auth = HTTPBasicAuth(username, password)
        if mappings_path:
            mappings_path = Path(mappings_path)
            if not mappings_path.is_file():
                logger.warning(
                    f"mappings_path '{mappings_path}' is not a Python module."
                )
            # intermediate variable to ensure path.append is possible so we'll never
            # path.pop a location that we didn't append
            mappings_folder = str(mappings_path.parent)
            sys.path.append(mappings_folder)
            mappings_module_name = mappings_path.stem
            try:
                mappings_module = import_module(mappings_module_name)
                self.in_use_mapping: Dict[str, Tuple[str, str]] = mappings_module.IN_USE_MAPPING
            except ImportError as exception:
                logger.debug(f"IN_USE_MAPPING was not imported: {exception}")
                self.in_use_mapping = {}
            finally:
                from DataDriver.openapi.dto_utils import add_dto_mixin, get_dto_class
                self.add_dto_mixin = add_dto_mixin
                self.get_dto_class = get_dto_class(
                    mappings_module_name=mappings_module_name
                )
                sys.path.pop()
        else:
            self.in_use_mapping = {}
            from DataDriver.openapi.dto_utils import add_dto_mixin, get_dto_class
            self.add_dto_mixin = add_dto_mixin
            self.get_dto_class = get_dto_class(mappings_module_name="no_mapping")

    @keyword
    def validate_openapi_document(self) -> None:
        errors_iterator = openapi_v3_spec_validator.iter_errors(self.openapi_doc)
        for error in errors_iterator:
            logger.error(error)
        validate_spec(self.openapi_doc)

    @keyword
    def test_unauthorized(self, endpoint: str, method: str) -> None:
        url = run_keyword("get_valid_url", endpoint)
        # logger.info(f"Sending unauthorized {method} request to {url}")
        response = self.session.request(
            method=method,
            url=url,
            verify=False,
        )
        assert response.status_code == 401

    @keyword
    def test_endpoint(self, method: str, endpoint: str, status_code: int) -> None:
        json_data: Optional[Dict[str, Any]] = None
        original_data: Optional[Dict[str, Any]] = None

        url: str = run_keyword("get_valid_url", endpoint)
        dto, schema = self.get_dto_and_schema(method=method, endpoint=endpoint)
        if dto and schema:
            dto = self.add_dto_mixin(dto=dto)
            json_data = asdict(dto)
            if status_code == 409:
                json_data = run_keyword("ensure_conflict", url, method, dto)
            if status_code in [400, 422]:
                json_data = dto.get_invalidated_data(schema, status_code)
        if status_code == 403:
            run_keyword("ensure_in_use", url)
        if status_code == 404:
            url = run_keyword("invalidate_url", url)
        if method == "PATCH":
            response: Response = run_keyword("authorized_request", url, "GET")
            if response.ok:
                original_data = response.json()
        response = self.authorized_request(method=method, url=url, json=json_data)
        if response.status_code != status_code:
            if not response.ok:
                if description := response.json().get("detail"):
                    pass
                else:
                    description = response.json().get("message")
                logger.error(
                    f"{response.reason}: {description}"
                )
            logger.info(
                f"\nSend: {_json.dumps(json_data, indent=4, sort_keys=True)}"
                f"\nGot: {_json.dumps(response.json(), indent=4, sort_keys=True)}"
            )
            raise AssertionError(
                f"Response status_code {response.status_code} was not {status_code}"
            )
        run_keyword("validate_response", endpoint, response, original_data)
        if method == "DELETE" and response.ok:
            response = run_keyword("authorized_request", url, "GET")
            if response.ok:
                raise AssertionError(
                    f"Resource still exists after deletion. Url was {url}"
                )
            # if the endpoint supports GET, 404 is expected, if not 405 is expected
            if response.status_code not in [404, 405]:
                logger.warning(
                    f"Unexpected response after deleting resource: Status_code "
                    f"{response.status_code} was received after trying to get {url} "
                    f"after sucessfully deleting it."
                )

    @keyword
    def get_valid_url(self, endpoint: str) -> str:
        endpoint_parts = list(endpoint.split("/"))
        for index, part in enumerate(endpoint_parts):
            if part.startswith("{") and part.endswith("}"):
                type_endpoint_parts = endpoint_parts[slice(index)]
                type_endpoint = "/".join(type_endpoint_parts)
                existing_id: str = run_keyword("get_valid_id_for_endpoint", type_endpoint)
                if not existing_id:
                    raise Exception
                endpoint_parts[index] = existing_id
        resolved_endpoint = "/".join(endpoint_parts)
        url = f"{self.base_url}{resolved_endpoint}"
        return url

    @keyword
    def get_valid_id_for_endpoint(self, endpoint: str) -> str:
        url = self.get_valid_url(endpoint=endpoint)
        # Try to create a new resource to prevent 403 and 409 conflicts caused by
        # operations performed on the same resource by other test cases
        try:
            dto, _ = self.get_dto_and_schema(endpoint=endpoint, method="POST")
            json_data = asdict(dto)
            response = self.authorized_request(method="POST", url=url, json=json_data)
        except NotImplementedError as exception:
            logger.debug(f"get_valid_id_for_endpoint POST failed: {exception}")
            # For endpoints that do no support POST, try to get an existing id using GET
            try:
                response = self.authorized_request(method="GET", url=url)
                assert response.ok
                response_data: Union[Dict[str, Any], List[Dict[str, Any]]] = response.json()
                if isinstance(response_data, list):
                    valid_ids: List[str] = [item["id"] for item in response_data]
                    logger.debug(
                        f"get_valid_id_for_endpoint: returning choice from list {valid_ids}"
                    )
                    return choice(valid_ids)
                if valid_id := response_data.get("id"):
                    logger.debug(f"get_valid_id_for_endpoint: returning {valid_id}")
                    return valid_id
                valid_ids = [item["id"] for item in response_data["items"]]
                logger.debug(
                    f"get_valid_id_for_endpoint: returning choice from items {valid_ids}"
                )
                return choice(valid_ids)
            except Exception as exception:
                logger.debug(
                    f"Failed to get a valid id using GET on {url}"
                    f"\nException was {exception}"
                )
                raise exception

        assert response.ok, (
            f"get_valid_id_for_endpoint received status_code {response.status_code}"
        )
        response_data = response.json()
        prepared_body: bytes = response.request.body
        send_json: Dict[str, Any] = _json.loads(prepared_body.decode("UTF-8"))
        # POST on /resource_type/{id}/array_item/ will return the updated {id} resource
        # instead of a newly created resource. In this case, the send_json must be
        # in the array of the 'array_item' property on {id}
        send_path: str = response.request.path_url
        response_path: Optional[str] = response_data.get("href", None)
        if response_path and send_path not in response_path:
            property_to_check = send_path.replace(response_path, "")[1:]
            item_list: List[Dict[str, Any]] = response_data[property_to_check]
            # Use the (mandatory) id to get the POSTed resource from the list
            [valid_id] = [item["id"] for item in item_list if item["id"] == send_json["id"]]
        else:
            valid_id: str = response_data["id"]
        return valid_id

    def get_dto_and_schema(
            self, endpoint: str, method: str
        ) -> Union[Tuple[Dto, Dict[str, Any]], Tuple[None, None]]:
        method = method.lower()
        # The endpoint can contain already resolved Ids that have to be matched
        # against the parametrized endpoints in the paths section.
        spec_endpoint = self.get_parametrized_endpoint(endpoint)
        try:
            method_spec = self.openapi_doc["paths"][spec_endpoint][method]
        except KeyError:
            raise NotImplementedError(f"method '{method}' not suported on '{spec_endpoint}")
        if (body_spec := method_spec.get("requestBody", None)) is None:
            return body_spec, None
        # Content should be a single key/value entry, so use tuple assignment
        content_type, = body_spec["content"].keys()
        if content_type != "application/json":
            # At present no supported for other types.
            raise NotImplementedError(f"content_type '{content_type}' not supported")
        content_schema = body_spec["content"][content_type]["schema"]
        resolved_schema: Dict[str, Any] = self.resolve_schema(content_schema)
        dto_class = self.get_dto_class(endpoint=spec_endpoint, method=method)
        dto_data = self.get_dto_data(
            schema=resolved_schema,
            dto=dto_class,
            operation_id=method_spec.get("operationId")
        )
        if dto_data is None:
            return None, None
        fields: List[Tuple[str, type]] = []
        for key, value in dto_data.items():
            fields.append((key, type(value)))
        dto_class = make_dataclass(
            cls_name=method_spec["operationId"],
            fields=fields,
            bases=(dto_class,),
        )
        dto_instance = dto_class(**dto_data)
        return dto_instance, resolved_schema

    def get_parametrized_endpoint(self, endpoint: str) -> str:
        def match_parts(parts: List[str], spec_parts: List[str]) -> bool:
            for part, spec_part in zip_longest(parts, spec_parts, fillvalue="Filler"):
                if part == "Filler" or spec_part == "Filler":
                    return False
                if part != spec_part and not spec_part.startswith("{"):
                    return False
            return True

        endpoint_parts = endpoint.split("/")
        # trailing '/' should not be matched
        if len(endpoint_parts) > 2 and endpoint_parts[-1] == "":
            endpoint_parts.pop(-1)
        spec_endpoints: List[str] = {**self.openapi_doc}["paths"].keys()
        for spec_endpoint in spec_endpoints:
            spec_endpoint_parts = spec_endpoint.split("/")
            if match_parts(endpoint_parts, spec_endpoint_parts):
                return spec_endpoint
        raise ValueError(f"{endpoint} not matched to openapi_doc path")

    @keyword
    def get_dto_data(
            self, schema: Dict[str, Any], dto: Type[Dto], operation_id: str
        ) -> Optional[Dict[str, Any]]:

        def get_constrained_values(property_name: str) -> List[Any]:
            constraints = dto.get_constraints()
            values = [
                c.values for c in constraints if (
                    isinstance(c, PropertyValueConstraint) and
                    c.property_name == property_name
                )
            ]
            # values should be empty or contain 1 list of allowed values
            return values.pop() if values else []

        def get_dependent_id(property_name: str, operation_id: str) -> Optional[str]:
            dependencies = dto.get_dependencies()
            # multiple get paths are possible based on the operation being performed
            id_get_paths = [
                (d.get_path, d.operation_id) for d in dependencies if (
                    isinstance(d, IdDependency) and
                    d.property_name == property_name
                )
            ]
            if not id_get_paths:
                return None
            if len(id_get_paths) == 1:
                id_get_path, _ = id_get_paths.pop()
            else:
                try:
                    [id_get_path] = [
                        path for path, operation in id_get_paths if operation == operation_id
                    ]
                # There could be multiple get_paths, but not one for the current operation
                except ValueError:
                    return None
            valid_id = self.get_valid_id_for_endpoint(endpoint=id_get_path)
            logger.debug(f"get_dependent_id for {id_get_path} returned {valid_id}")
            return valid_id


        json_data: Dict[str, Any] = {}

        for property_name in schema.get("properties", []):
            property_type = schema["properties"][property_name]["type"]
            if constrained_values := get_constrained_values(property_name):
                json_data[property_name] = choice(constrained_values)
                continue
            if dependent_id := get_dependent_id(
                property_name=property_name, operation_id=operation_id
            ):
                json_data[property_name] = dependent_id
                continue
            if property_type == "boolean":
                json_data[property_name] = bool(getrandbits(1))
                continue
            # if the property specifies an enum, pick one at random
            if from_enum := schema["properties"	][property_name].get("enum", None):
                value = choice(from_enum)
                json_data[property_name] = value
                continue
            # Use int32 integers if "format" does not specify int64
            if property_type == "integer":
                property_format = schema["properties"][property_name].get("format", "int32")
                if property_format == "int64":
                    min_int = -9223372036854775808
                    max_int = 9223372036854775807
                else:
                    min_int = -2147483648
                    max_int = 2147483647
                #TODO: add support for exclusiveMinimum and exclusiveMaximum
                minimum = schema["properties"][property_name].get("minimum", min_int)
                maximum = schema["properties"][property_name].get("maximum", max_int)
                value = randint(minimum, maximum)
                json_data[property_name] = value
                continue
            # Python floats are already double precision, so no check for "format"
            if property_type == "number":
                minimum = schema["properties"][property_name].get("minimum", 0.0)
                maximum = schema["properties"][property_name].get("maximum", 1.0)
                value = uniform(minimum, maximum)
                json_data[property_name] = value
                continue
            #TODO: byte, binary, date, date-time based on "format"
            if property_type == "string":
                minimum = schema["properties"][property_name].get("minLength", 0)
                maximum = schema["properties"][property_name].get("maxLength", 36)
                value = uuid4().hex
                while len(value) < minimum:
                    value = value + uuid4().hex
                if len(value) > maximum:
                    value = value[:maximum]
                json_data[property_name] = value
                continue
            if property_type == "object":
                #FIXME: user implemented Dto should not depend on endpoint and method
                default_dto = self.get_dto_class(endpoint="", method="")
                object_data = self.get_dto_data(
                    schema=schema["properties"][property_name],
                    dto=default_dto,
                    operation_id="",
                )
                json_data[property_name] = object_data
                continue
            raise NotImplementedError(f"Type '{property_type}' is currently not supported")
        return json_data

    @staticmethod
    @keyword
    def invalidate_url(valid_url: str) -> str:
        url_parts = list(valid_url.split("/"))
        for part in reversed(url_parts):
            if len(part) > 30:
                invalid_url = valid_url.replace(part, part[1:])
                return invalid_url
        raise Exception(f"Failed to invalidate {valid_url}")

    @keyword
    def ensure_in_use(self, url: str) -> None:
        endpoint = url.removeprefix(self.base_url)
        endpoint_parts = endpoint.split("/")
        # first part will be '' since an endpoint starts with /
        endpoint_parts.pop(0)
        parameterized_url = self.get_parametrized_endpoint(endpoint=endpoint)
        if parameterized_url.endswith("}"):
            resource_type = endpoint_parts[-2]
            resource_id = endpoint_parts[-1]
        else:
            resource_type = endpoint_parts[-1]
            resource_id = None
        post_endpoint, property_name = self.in_use_mapping[resource_type]
        dto, _ = self.get_dto_and_schema(method="POST", endpoint=post_endpoint)
        json_data = asdict(dto)
        if resource_id:
            json_data[property_name] = resource_id
        post_url = self.get_valid_url(endpoint=post_endpoint)
        response = self.authorized_request(method="POST", url=post_url, json=json_data)
        if not response.ok:
            logger.debug(
                f"POST on {post_url} with json {json_data} failed: {response.json()}"
            )
            response.raise_for_status()

    @keyword
    def ensure_conflict(self, url: str, method: str, dto: Dto) -> Dict[str, Any]:
        json_data = asdict(dto)
        for constraint in dto.get_constraints():
            if isinstance(constraint, UniquePropertyValueConstraint):
                json_data[constraint.property_name] = constraint.value
                # create a new resource that the original request will conflict with
                if method in ["PATCH", "PUT"]:
                    post_url_parts = url.split("/")[:-1]
                    post_url = "/".join(post_url_parts)
                else:
                    post_url = url
                response = self.authorized_request(
                    method="POST", url=post_url, json=json_data
                )
                # conflicting resource may already exist, so 409 is also valid
                assert response.ok or response.status_code == 409, (
                    f"ensure_conflict received {response.status_code}: {response.json()}"
                )
                return json_data
        try:
            response = self.authorized_request(method="GET", url=url)
            response_json = response.json()
            # update the values in the json_data with the values from the response
            for key in json_data.keys():
                json_data[key] = response_json[key]
            return json_data
        except Exception:
            # couldn't retrieve a resource to conflict with, so create one instead
            response = self.authorized_request(method="POST", url=url, json=json_data)
            assert response.ok, (
                f"ensure_conflict received {response.status_code}: {response.json()}"
            )
            return json_data

    def resolve_schema(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        # schema is mutable, so copy to prevent mutation of original schema argument
        resolved_schema: Dict[str, Any] = schema.copy()
        if schema_parts := resolved_schema.pop("allOf", None):
            for schema_part in schema_parts:
                resolved_part = self.resolve_schema(schema_part)
                resolved_schema = self._merge_schemas(resolved_schema, resolved_part)
        return resolved_schema

    @staticmethod
    def _merge_schemas(first: Dict[str, Any], second: Dict[str, Any]) -> Dict[str, Any]:
        merged_schema = first.copy()
        for key, value in second.items():
            # for exisiting keys, merge dict and list values, leave others unchanged
            if key in merged_schema.keys():
                if isinstance(value, dict):
                    # if the key holds a dict, merge the values (e.g. 'properties')
                    merged_schema[key].update(value)
                elif isinstance(value, list):
                    # if the key holds a list, extend the values (e.g. 'required')
                    merged_schema[key].extend(value)
                else:
                    logger.debug(
                        f"key '{key}' with value '{merged_schema[key]}' not "
                        f"updated to '{value}'"
                    )
            else:
                merged_schema[key] = value
        return merged_schema

    @keyword
    def validate_response(
            self,
            endpoint: str,
            response: Response,
            original_data: Optional[Dict[str, Any]] = None,
        ) -> None:
        response_spec = self.get_response_spec(
            endpoint=endpoint,
            method=response.request.method,
            status_code=response.status_code,
        )
        if response.status_code == 204:
            assert not response.content
            return
        # content should be a single key/value entry, so use tuple assignment
        content_type, = response_spec["content"].keys()
        content_schema, = response_spec["content"].values()
        if content_type == "application/json":
            jsonschema.validate(instance=response.content, schema=content_schema)
        else:
            # At present, only json is supported.
            raise NotImplementedError(f"content_type '{content_type}' not supported")
        if response.headers["Content-Type"] != content_type:
            raise ValueError(
                f"Content-Type '{response.headers['Content-Type']}' of the response "
                f"is not '{content_type}' as specified in the OpenAPI document."
            )
        json_response = response.json()
        # ensure the href is valid
        if "href" in json_response:
            url = f"{self.origin}{json_response['href']}"
            get_response = self.authorized_request(method="GET", url=url)
            assert get_response.json() == json_response, (
                f"{get_response.json()} not equal to original {json_response}"
            )
        # if the response contains a resource, perform additional validations
        if isinstance(json_response, dict):
            # every property that was sucessfully send must be in the response and
            # the value in the response must be the value that was send
            if response.ok and response.request.method in ["POST", "PUT", "PATCH"]:
                self.validate_send_response(response=response, original_data=original_data)
            # ensure string properties are not empty
            failed_keys: List[str] = []
            for key, value in json_response.items():
                if isinstance(value, str) and value.isspace():
                    failed_keys.append(key)
            if failed_keys:
                raise AssertionError(
                f"Properties {', '.join(failed_keys)} contain a whitespace value"
            )

    @staticmethod
    @keyword
    def validate_send_response(
            response: Response,
            original_data: Optional[Dict[str, Any]] = None
        ) -> None:
        reference = response.json()
        prepared_body: bytes = response.request.body
        send_json: Dict[str, Any] = _json.loads(prepared_body.decode("UTF-8"))
        # POST on /resource_type/{id}/array_item/ will return the updated {id} resource
        # instead of a newly created resource. In this case, the send_json must be
        # in the array of the 'array_item' property on {id}
        send_path: str = response.request.path_url
        response_path = reference.get("href", None)
        if response_path and send_path not in response_path:
            property_to_check = send_path.replace(response_path, "")[1:]
            if isinstance(reference[property_to_check], list):
                item_list: List[Dict[str, Any]] = reference[property_to_check]
                # Use the (mandatory) id to get the POSTed resource from the list
                [reference] = [item for item in item_list if item["id"] == send_json["id"]]
        for key, value in send_json.items():
            try:
                if value is None:
                    # if a None value is send, the target property should be cleared or
                    # reverted to the default value which depends on its type
                    assert reference[key] in [None, [], 1, False, ""], (
                        f"Received value for {key} '{reference[key]}' does not "
                        f"match '{value}' in the {response.request.method} request"
                        f"\nSend: {_json.dumps(send_json, indent=4, sort_keys=True)}"
                        f"\nGot: {_json.dumps(reference, indent=4, sort_keys=True)}"
                    )
                else:
                    assert reference[key] == value, (
                        f"Received value for {key} '{reference[key]}' does not "
                        f"match '{value}' in the {response.request.method} request"
                        f"\nSend: {_json.dumps(send_json, indent=4, sort_keys=True)}"
                        f"\nGot: {_json.dumps(reference, indent=4, sort_keys=True)}"
                    )
            except KeyError:
                raise AssertionError(
                    f"{key} was {response.request.method} with value '{value}' "
                    f"but not present in the response: {reference}"
                    f"\nSend: {_json.dumps(send_json, indent=4, sort_keys=True)}"
                    f"\nGot: {_json.dumps(reference, indent=4, sort_keys=True)}"
                )
        # In case of PATCH requests, ensure that only send properties have changed
        if original_data:
            for key, value in original_data.items():
                if key not in send_json.keys():
                    try:
                        assert value == reference[key], (
                            f"Received value for {key} '{reference[key]}' does not "
                            f"match '{value}' in the pre-patch data\nPre-patch: "
                            f"{_json.dumps(original_data, indent=4, sort_keys=True)}"
                            f"\nGot: {_json.dumps(reference, indent=4, sort_keys=True)}"
                        )
                    except KeyError:
                        raise AssertionError(
                            f"{key} was with value '{value}' was no longer "
                            f"present in the response: {reference}\nPre-patch: "
                            f"{_json.dumps(original_data, indent=4, sort_keys=True)}"
                            f"\nGot: {_json.dumps(reference, indent=4, sort_keys=True)}"
                        )

    def get_response_spec(
            self, endpoint: str, method: str, status_code: int
        ) -> Dict[str, Any]:
        method = method.lower()
        status = str(status_code)
        spec = {**self.openapi_doc}["paths"][endpoint][method]["responses"][status]
        return spec

    @keyword
    def authorized_request(
            self,
            url: str,
            method: str,
            json: Optional[Any] = None,
        ) -> Response:
        logger.info(f"Sending {method} request to {url}")
        response = self.session.request(
            method=method,
            url=url,
            json=json,
            auth=self.auth,
            verify=False,
        )
        return response


# Support Robot Framework import mechanism
openapi_executors = OpenapiExecutors    # pylint: disable=invalid-name
