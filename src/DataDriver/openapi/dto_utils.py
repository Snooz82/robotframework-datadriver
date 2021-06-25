from logging import getLogger
from typing import Any, Dict, Type
from uuid import uuid4

from .dto_base import Dto

logger = getLogger(__name__)


#TODO: does not belong here, how to handle user-provided business logic?
from .user_specific.usermanagement_dtos import DeviceGroupSendDto, RoleItemDto
USERMANAGEMENT_DTO_MAPPING = {
    (r"/deviceGroups", "post"): DeviceGroupSendDto,
    (r"/deviceGroups/{deviceGroupId}", "patch"): DeviceGroupSendDto,
    (r"/deviceGroups/{deviceGroupId}", "put"): DeviceGroupSendDto,
    (r"/roles/{roleId}/deviceGroups", "post"): RoleItemDto,
    (r"/roles/{roleId}/fixedLayouts", "post"): RoleItemDto,
    (r"/roles/{roleId}/functions", "post"): RoleItemDto,
    (r"/roles/{roleId}/layouts", "post"): RoleItemDto,
    (r"/roles/{roleId}/monitors", "post"): RoleItemDto,
    (r"/roles/{roleId}/multiLayouts", "post"): RoleItemDto,
    (r"/roles/{roleId}/servers", "post"): RoleItemDto,
    (r"/roles/{roleId}/users", "post"): RoleItemDto,
    (r"/roles/{roleId}/viewerMacros", "post"): RoleItemDto,
}

class DtoMixin:
    def set_minimum_data(self) -> None:
        raise NotImplementedError

    def set_complete_data(self) -> None:
        raise NotImplementedError

    def set_partial_data(self) -> None:
        raise NotImplementedError

    def get_invalidated_data(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        properties: Dict[str, Any] = self.__dict__
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

def get_dto_class(endpoint: str, method: str) -> Type[Dto]:
    try:
        return USERMANAGEMENT_DTO_MAPPING[(endpoint, method)]
    except KeyError:
        return Dto
