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

from abc import ABC
from dataclasses import dataclass
from typing import Any, List, Optional


class Constraint(ABC):
    pass


class Dependency(ABC):
    pass


@dataclass
class Dto:
    @staticmethod
    def get_dependencies() -> List[Dependency]:
        return []

    @staticmethod
    def get_constraints() -> List[Constraint]:
        return []


@dataclass
class PropertyValueConstraint(Constraint):
    """The allowed values for property_name."""
    property_name: str
    values: List[Any]


@dataclass
class IdDependency(Dependency):
    """The path where a valid id for the propery_name can be gotten (using GET)"""
    property_name: str
    get_path: str
    operation_id: Optional[str] = None


@dataclass
class UniquePropertyValueConstraint(Constraint):
    """The value of the property must be unique within the resource scope."""
    property_name: str
    value: Any
