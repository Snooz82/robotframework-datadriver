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

from importlib import import_module
from logging import getLogger
from random import randint, uniform
from typing import Any, Dict, List, Tuple, Type
from uuid import uuid4

from DataDriver.openapi.dto_base import Dto

logger = getLogger(__name__)


class DtoMixin:
    def set_minimum_data(self) -> None:
        raise NotImplementedError

    def set_complete_data(self) -> None:
        raise NotImplementedError

    def set_partial_data(self) -> None:
        raise NotImplementedError

    def get_invalidated_data(
            self, schema: Dict[str, Any], status_code: int
        ) -> Dict[str, Any]:
        properties: Dict[str, Any] = self.__dict__
        # if there are dependencies and / or constraints, change the (valid) values
        # to random values
        constrained_properties: List[str] = []
        constrained_properties += [d.property_name for d in self.get_dependencies()]
        constrained_properties += [c.proprety_name for c in self.get_constraints()]
        # for status 400, invalidate a constraint but send otherwise valid data
        if constrained_properties and status_code == 400:
            for property_to_invalidate in constrained_properties:
                property_data = schema["properties"][property_to_invalidate]
                property_type = property_data["type"]
                current_value = properties[property_to_invalidate]
                if property_type == "boolean":
                    properties[property_to_invalidate] = not current_value
                    continue
                if property_type == "integer":
                    minimum = property_data.get("minimum", -2147483648)
                    maximum = property_data.get("maximum", 2147483647)
                    value = randint(minimum, maximum)
                    properties[property_to_invalidate] = value
                    continue
                if property_type == "number":
                    minimum = property_data.get("minimum", 0.0)
                    maximum = property_data.get("maximum", 1.0)
                    value = uniform(minimum, maximum)
                    properties[property_to_invalidate] = value
                    continue
                if property_type == "string":
                    minimum = property_data.get("minLength", 0)
                    maximum = property_data.get("maxLength", 36)
                    value = uuid4().hex
                    while len(value) < minimum:
                        value = value + uuid4().hex
                    if len(value) > maximum:
                        value = value[:maximum]
                    properties[property_to_invalidate] = value
                    continue
            return properties
        # for status 422 or if there are no constraints, send invalid data
        # For all properties that require a type other than a string, set a string
        schema_properties = schema["properties"]
        for property_name, property_values in schema_properties.items():
            property_type = property_values.get("type")
            if property_type != "string":
                logger.debug(
                    f"property {property_name} set to str instead of {property_type}"
                )
                properties[property_name] = uuid4().hex
            else:
                # Since int / float / bool can always be interpreted as sting,
                # change the string to a nested object
                properties[property_name] = [
                    {
                        "invalid": [
                            None
                        ]
                    }
                ]
        return properties


class ExtendedDto(Dto, DtoMixin):
    pass


def add_dto_mixin(dto: Dto) -> ExtendedDto:
    """Add the DtoMixin to a Dto class instance"""
    base_cls = dto.__class__
    base_cls_name = dto.__class__.__name__
    dto.__class__ = type(base_cls_name, (base_cls, DtoMixin),{})
    return dto


class get_dto_class:
    def __init__(self, mappings_module_name: str) -> None:
        try:
            mappings_module = import_module(mappings_module_name)
            self.dto_mapping: Dict[Tuple[str, str], Any] = mappings_module.DTO_MAPPING
        except (ImportError, AttributeError) as exception:
            logger.debug(f"DTO_MAPPING was not imported: {exception}")
            self.dto_mapping = {}

    def __call__(self, endpoint: str, method: str) -> Type[Dto]:
        try:
            return self.dto_mapping[(endpoint, method)]
        except KeyError:
            return Dto
