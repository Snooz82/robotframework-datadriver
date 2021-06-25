from abc import ABC
from dataclasses import dataclass
from typing import Any, List


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
    operation_id: str
    get_path: str


@dataclass
class UniquePropertyValueConstraint(Constraint):
    """The value of the property must be unique within the resource scope."""

    property_name: str
    value: Any
