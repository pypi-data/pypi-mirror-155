import cjen
from cjen.sco.step_definitions import StepDefinitions

from eclinical import PortalLoginService, Environment
from eclinical.standard.portal.dto.role_rel_user import RoleRelUsers
from eclinical.standard.portal.dto.user_roles import UserRoles


class UserRole(PortalLoginService):
    def __init__(self, environment: Environment = None):
        super().__init__(environment)
        self.step_definitions = StepDefinitions()

    # [{"roleId": 191, "roleCode": "PI/PI", "userGroupUserRelId": 657, "id": 2278, "loginName": "houyu", "userGroupName": "edetek"},
    # {"roleId": 191, "roleCode": "PI/PI", "userGroupUserRelId": 664, "id": 2286, "loginName": "CPC01", "userGroupName": "edetek"}]
    @cjen.http.post_mapping(uri="admin/role/{role_id}/user_group_user")
    def api_user_group_user(self, path_variable, data, resp=None, **kwargs):
        ...

    # {"roleId": 191}
    @cjen.http.post_mapping(uri="admin/role/{role_id}/relation/user_group_users?pageNo={pageNo}&pageSize=25")
    def get_relations_users(self, path_variable, data, resp=None, **kwargs):
        ...

    # {"roleId":191
    @cjen.http.post_mapping(uri="admin/role/{role_id}/no_relation/user_group_users?pageNo={pageNo}&pageSize=25", json_clazz=RoleRelUsers)
    def get_no_relations_users(self, path_variable, data, users: RoleRelUsers, resp=None, **kwargs):
        from eclinical.standard.steps.portal.user_roles.portal_find_no_rel_user import PortalFindNoRelUser
        self.step_definitions.call_back(PortalFindNoRelUser.Name, users=users)
        if not self.context[PortalFindNoRelUser.Id]:
            if not users.nextPage() == 0:
                self.api_get_user_roles(path_variable=dict(pageNo=users.nextPage(), role_id=path_variable.get("role_id")))

    @cjen.http.get_mapping(uri="admin/role/user_roles?pageNo={pageNo}&pageSize=25", json_clazz=UserRoles)
    def api_get_user_roles(self, path_variable, user_role: UserRoles = None, resp=None, **kwargs):
        from eclinical.standard.steps.portal.user_roles.portal_get_user_role import PortalGetUserRole
        self.step_definitions.call_back(PortalGetUserRole.Name, user_role=user_role)
        if not self.context[PortalGetUserRole.Id]:
            if not user_role.nextPage() == 0:
                self.api_get_user_roles(path_variable=dict(pageNo=user_role.nextPage()))
