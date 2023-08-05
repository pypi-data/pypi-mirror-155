# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class SystemUserRoleResponse(Model):
    """SystemUserRoleResponse.

    :param system_user_role_id:
    :type system_user_role_id: int
    :param system_user_role_name:
    :type system_user_role_name: str
    :param description:
    :type description: str
    :param users_assigned_count:
    :type users_assigned_count: int
    :param permissions:
    :type permissions: ~energycap.sdk.models.Permissions
    :param read_only:
    :type read_only: bool
    """

    _attribute_map = {
        'system_user_role_id': {'key': 'systemUserRoleId', 'type': 'int'},
        'system_user_role_name': {'key': 'systemUserRoleName', 'type': 'str'},
        'description': {'key': 'description', 'type': 'str'},
        'users_assigned_count': {'key': 'usersAssignedCount', 'type': 'int'},
        'permissions': {'key': 'permissions', 'type': 'Permissions'},
        'read_only': {'key': 'readOnly', 'type': 'bool'},
    }

    def __init__(self, *, system_user_role_id: int=None, system_user_role_name: str=None, description: str=None, users_assigned_count: int=None, permissions=None, read_only: bool=None, **kwargs) -> None:
        super(SystemUserRoleResponse, self).__init__(**kwargs)
        self.system_user_role_id = system_user_role_id
        self.system_user_role_name = system_user_role_name
        self.description = description
        self.users_assigned_count = users_assigned_count
        self.permissions = permissions
        self.read_only = read_only
