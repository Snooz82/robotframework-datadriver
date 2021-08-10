# pylint: disable=invalid-name
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from DataDriver.openapi.dto_base import (
    Constraint,
    Dependency,
    Dto,
    IdDependency,
    PropertyValueConstraint,
    UniquePropertyValueConstraint,
)

IN_USE_MAPPING: Dict[str, str] = {
    "wagegroups": "/employees/",
}