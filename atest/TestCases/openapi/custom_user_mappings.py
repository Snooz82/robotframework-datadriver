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


@dataclass
class EmployeeDto(Dto):
    @staticmethod
    def get_dependencies() -> List[Dependency]:
        dependencies = [
            IdDependency(
                property_name="wagegroup_id",
                get_path="/wagegroups",
            ),
        ]
        return dependencies


DTO_MAPPING: Dict[Tuple[Any, Any], Any] = {
    (r"/employees", "post"): EmployeeDto,
}


IN_USE_MAPPING: Dict[str, Tuple[str, str]] = {
    # deliberate trailing / to validate redirect matching
    "wagegroups": ("/employees/", "wagegroup_id"),
}
