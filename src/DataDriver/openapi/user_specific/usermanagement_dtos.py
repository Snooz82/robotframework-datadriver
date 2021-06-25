# pylint: disable=invalid-name
from dataclasses import dataclass
from typing import List

from ..dto_base import (
    Constraint,
    Dependency,
    Dto,
    IdDependency,
    PropertyValueConstraint,
    UniquePropertyValueConstraint,
)


@dataclass
class DeviceGroupSendDto(Dto):
    @staticmethod
    def get_constraints() -> List[Constraint]:
        unique_name = UniquePropertyValueConstraint(
            property_name="name",
            value="Highlander"
        )
        return [unique_name]


@dataclass
class RoleItemDto(Dto):
    @staticmethod
    def get_dependencies() -> List[Dependency]:
        dependencies = [
            IdDependency(
                operation_id="postRoleDeviceGroup",
                get_path="/deviceGroups",
            ),
            IdDependency(
                operation_id="postRoleFixedLayout",
                get_path="/fixedLayouts",
            ),
            IdDependency(
                operation_id="postRoleFunction",
                get_path="/functions",
            ),
            IdDependency(
                operation_id="postRoleLayout",
                get_path="/layouts",
            ),
            IdDependency(
                operation_id="postRoleMonitor",
                get_path="/monitors",
            ),
            IdDependency(
                operation_id="postRoleMultiLayout",
                get_path="/multiLayouts",
            ),
            IdDependency(
                operation_id="postRoleServer",
                get_path="/servers",
            ),
            IdDependency(
                operation_id="postRoleUser",
                get_path="/users",
            ),
            IdDependency(
                operation_id="postRoleViewerMacro",
                get_path="/viewerMacros",
            ),
        ]
        return dependencies
