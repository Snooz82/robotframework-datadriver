import json as _json
import random
from dataclasses import asdict, make_dataclass
from itertools import zip_longest
from logging import getLogger
from random import choice, randint
from typing import Any, Dict, List, Optional, Tuple, Type, Union
from uuid import uuid4

import jsonschema
import openapi_core
from openapi_core.spec.paths import SpecPath
from openapi_spec_validator import openapi_v3_spec_validator, validate_spec
from requests import Response, Session
from requests.auth import HTTPBasicAuth
from robot.api.deco import keyword, library

from .dto_base import (
    IdDependency,
    PropertyValueConstraint,
    UniquePropertyValueConstraint,
)
from .dto_utils import Dto, add_dto_mixin, get_dto_class


logger = getLogger(__name__)


#TODO: does not belong here, how to handle user-provided business logic?
IN_USE_MAPPING = {
    "deviceGroups": "/roles/{roleId}/deviceGroups",
    "users": "/roles/{roleId}/users",
    "roles": "/roles/{roleId}/deviceGroups",
}


@library(scope="GLOBAL")
class openapi_runner:
    """
    Module providing some keywords that can be used in test templates using
    test case data generated from the openapi_reader.
    """
    def __init__(self, openapi_doc: Dict[str, Any], base_url: str, user: str = "", password: str = "") -> None:
        self.openapi_doc = openapi_doc  #TODO: should be set by openapi_reader
        self.session = Session()
        self.base_url = base_url
        self.auth = HTTPBasicAuth(user, password)
        self.spec: SpecPath = openapi_core.create_spec(self.openapi_doc)

    @keyword
    def validate_openapi_document(self) -> None:
        errors_iterator = openapi_v3_spec_validator.iter_errors(self.openapi_doc)
        for error in errors_iterator:
            logger.error(error)
        validate_spec(self.openapi_doc)

    @keyword
    def test_unauthorized(self, method: str, endpoint: str) -> None:
        url = self.get_valid_url(endpoint)
        logger.info(f"Sending {method} request to {url}")
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

        url = self.get_valid_url(method=method, endpoint=endpoint)
        dto, schema = self.get_dto_and_schema(method=method, endpoint=endpoint)
        if dto:
            dto = add_dto_mixin(dto=dto)
            json_data = asdict(dto)
            if status_code == 409 and dto:
                json_data = self.ensure_conflict(url=url, dto=dto, method=method)
            if status_code == 400 and dto:
                json_data = dto.get_invalidated_data(schema)
        if status_code == 403:
            self.ensure_in_use(url)
        if status_code == 404:
            url = self.invalidate_url(url)
        if method == "PATCH":
            response = self.authorized_request(method="GET", url=url)
            # The /users/{userId}/password can be PATCHed but GET is not allowed
            if response.status_code != 405:
                original_data = response.json()
        response = self.authorized_request(method=method, url=url, json=json_data)
        if response.status_code != status_code:
            if not response.ok:
                logger.error(
                    f"{response.reason}: {response.json().get('message')}"
                )
            logger.info(
                f"\nSend: {_json.dumps(json_data, indent=4, sort_keys=True)}"
                f"\nGot: {_json.dumps(response.json(), indent=4, sort_keys=True)}"
            )
            raise AssertionError(
                f"Response status_code {response.status_code} was not {status_code}"
            )
        self.validate_response(endpoint=endpoint, response=response, original_data=original_data)

    def get_valid_url(self, endpoint: str, method: str = "") -> str:
        endpoint_parts = list(endpoint.split("/"))
        for index, part in enumerate(endpoint_parts):
            if part.startswith("{") and part.endswith("}"):
                type_endpoint_parts = endpoint_parts[slice(index)]
                type_endpoint = "/".join(type_endpoint_parts)
                existing_id = self.get_valid_id_for_endpoint(
                    endpoint=type_endpoint, method=method
                )
                if not existing_id:
                    raise Exception
                endpoint_parts[index] = existing_id
        resolved_endpoint = "/".join(endpoint_parts)
        url = f"{self.base_url}{resolved_endpoint}"
        return url

    def get_valid_id_for_endpoint(self, endpoint: str, method: str = "") -> str:
        url = self.get_valid_url(endpoint=endpoint, method=method)
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
                assert response.status_code == 200
                response_data = response.json()
                if isinstance(response_data, list):
                    valid_ids: List[str] = [item["id"] for item in response_data]
                    return choice(valid_ids)
                if valid_id := response_data.get("id"):
                    return valid_id
                valid_ids = [item["id"] for item in response_data["items"]]
                return choice(valid_ids)
            except Exception as exception:
                logger.debug(
                    f"Failed to get a valid id using GET on {url}"
                    f"\nException was {exception}"
                )
                raise exception

        assert response.status_code == 201, (
            f"get_valid_id_for_endpoint received status_code {response.status_code}"
        )
        response_data = response.json()
        prepared_body: bytes = response.request.body
        send_json: Dict[str, Any] = _json.loads(prepared_body.decode("UTF-8"))
        # POST on /resource_type/{id}/array_item/ will return the updated {id} resource
        # instead of a newly created resource. In this case, the send_json must be
        # in the array of the 'array_item' property on {id}
        send_path: str = response.request.path_url
        response_path = response_data["href"]
        if send_path not in response_path:
            property_to_check = send_path.replace(response_path, "")[1:]
            item_list: List[Dict[str, Any]] = response_data[property_to_check]
            # Use the (mandatory) id to get the POSTed resource from the list
            [valid_id] = [item["id"] for item in item_list if item["id"] == send_json["id"]]
        else:
            valid_id = response_data["id"]
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
        # content should be a single key/value entry, so use tuple assignment
        content_type, = body_spec["content"].keys()
        if content_type != "application/json":
            # At present, all endpoints use json so no supported for other types.
            raise NotImplementedError(f"content_type '{content_type}' not supported")
        content_schema = body_spec["content"][content_type]["schema"]
        resolved_schema: Dict[str, Any] = self.resolve_schema(content_schema)
        dto_class = get_dto_class(endpoint=spec_endpoint, method=method)
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
                if part != spec_part and not spec_part.startswith("{"):
                    return False
            return True

        endpoint_parts = endpoint.split("/")
        spec_endpoints: List[str] = {**self.openapi_doc}["paths"].keys()
        for spec_endpoint in spec_endpoints:
            spec_endpoint_parts = spec_endpoint.split("/")
            if match_parts(endpoint_parts, spec_endpoint_parts):
                return spec_endpoint
        raise ValueError(f"{endpoint} not matched to openapi_doc path")

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

        def get_dependent_id(operation_id: str) -> Optional[str]:
            dependencies = dto.get_dependencies()
            id_get_path = [
                d.get_path for d in dependencies if (
                    isinstance(d, IdDependency) and
                    d.operation_id == operation_id
                )
            ]
            # if an id reference is found, it can only be one (resources are unique)
            if id_get_path:
                return self.get_valid_id_for_endpoint(endpoint=id_get_path.pop())
            return None

        json_data: Dict[str, Any] = {}

        for property_name in schema.get("properties", []):
            property_type = schema["properties"][property_name]["type"]
            if constrained_values := get_constrained_values(property_name):
                json_data[property_name] = choice(constrained_values)
                continue
            if property_name == "id":
                if dependent_id := get_dependent_id(operation_id):
                    json_data[property_name] = dependent_id
                    continue
            if property_type == "string":
                json_data[property_name] = uuid4().hex
                continue
            if property_type == "integer":
                minimum = schema["properties"][property_name].get("minimum")
                maximum = schema["properties"][property_name].get("maximum")
                value = self.get_random_int(minimum=minimum, maximum=maximum)
                json_data[property_name] = value
                continue
            if property_type == "boolean":
                json_data[property_name] = bool(random.getrandbits(1))
                continue
            raise NotImplementedError(f"{property_type}")
        return json_data

    @staticmethod
    def get_random_int(minimum: Optional[int], maximum: Optional[int]) -> int:
        if minimum is None:
            minimum = 0
        if maximum is None:
            maximum = uuid4().int
        return randint(minimum, maximum)

    @staticmethod
    def invalidate_url(valid_url: str) -> str:
        url_parts = list(valid_url.split("/"))
        for part in reversed(url_parts):
            if len(part) > 30:
                invalid_url = valid_url.replace(part, part[1:])
                return invalid_url
        raise Exception(f"Failed to invalidate {valid_url}")

    def ensure_in_use(self, url: str) -> None:
        url_parts = url.split("/")
        resource_type = url_parts[-2]
        resource_id = url_parts[-1]
        post_endpoint = IN_USE_MAPPING[resource_type]
        dto, _ = self.get_dto_and_schema(method="POST", endpoint=post_endpoint)
        json_data = asdict(dto)
        if resource_type != "roles":
            json_data["id"] = resource_id
            post_url = self.get_valid_url(endpoint=post_endpoint)
        else:
            post_url = f"{url}/deviceGroups"
        response = self.authorized_request(url=post_url, method="POST", json=json_data)
        assert response.status_code == 201

    def ensure_conflict(self, url: str, dto: Dto, method: str) -> Dict[str, Any]:
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
                assert response.status_code in [201, 409], (
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
            assert response.status_code == 201, (
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
            # At present, all endpoints use json so no supported for other types.
            raise NotImplementedError(f"content_type '{content_type}' not supported")
        if response.headers["Content-Type"] != content_type:
            raise ValueError(
                f"Content-Type '{response.headers['Content-Type']}' of the response "
                f"is not '{content_type}' as specified in the OpenAPI document."
            )
        json_response = response.json()
        # ensure the href is valid
        if "href" in json_response:
            url = f"{self.url_base}{json_response['href']}"
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
        response_path = reference["href"]
        if send_path not in response_path:
            property_to_check = send_path.replace(response_path, "")[1:]
            if isinstance(reference[property_to_check], list):
                item_list: List[Dict[str, Any]] = reference[property_to_check]
                # Use the (mandatory) id to get the POSTed resource from the list
                [reference] = [item for item in item_list if item["id"] == send_json["id"]]
        for key, value in send_json.items():
            # the received password value is the password hash so comparing to the send
            # value will always fail
            if key == "password":
                continue
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
                            f"match '{value}' in the pre-patch data"
                            f"\nPre-patch: {_json.dumps(original_data, indent=4, sort_keys=True)}"
                            f"\nGot: {_json.dumps(reference, indent=4, sort_keys=True)}"
                        )
                    except KeyError:
                        raise AssertionError(
                            f"{key} was with value '{value}' was no longer "
                            f"present in the response: {reference}"
                            f"\nPre-patch: {_json.dumps(original_data, indent=4, sort_keys=True)}"
                            f"\nGot: {_json.dumps(reference, indent=4, sort_keys=True)}"
                        )

    def get_response_spec(self, endpoint: str, method: str, status_code: int) -> Dict[str, Any]:
        method = method.lower()
        status = str(status_code)
        spec = {**self.openapi_doc}["paths"][endpoint][method]["responses"][status]
        return spec

    def get_openapi_doc(self) -> Dict[str, Any]:
        return self.openapi_doc

    def authorized_request(
            self,
            method: str,
            url: str,
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
