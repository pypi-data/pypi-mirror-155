import cjen
from cjen.sco.step_definitions import StepDefinitions

from eclinical import PortalLoginService, Environment
from eclinical.standard.base.ok_response import OkResponse
from eclinical.standard.portal.dto.query_user_groups import QueryUserGroups
from eclinical.standard.portal.dto.role_list import RoleList
from eclinical.standard.portal.dto.user_access import UserAccess
from eclinical.standard.portal.dto.user_group_role_rel import UserGroupRoleRel
from eclinical.standard.portal.dto.users import Users


class User(PortalLoginService):
    def __init__(self, environment: Environment = None):
        super().__init__(environment)
        self.step_definitions = StepDefinitions()

    @cjen.http.put_mapping(uri="admin/user/{user_id}/study_title?sendEmail=false", json_clazz=OkResponse)
    def api_study_title(self, path_variable, data, ok: OkResponse = None, resp=None, **kwargs):
        ...

    @cjen.http.get_mapping(uri="admin/user/{user_id}/access_list", json_clazz=UserAccess)
    def api_user_access(self, path_variable, user_access: UserAccess = None, resp=None, **kwargs):
        from eclinical.standard.steps.portal.user.portal_user_access import PortalUserAccess
        self.step_definitions.call_back(PortalUserAccess.Name, user_access=user_access)

    @cjen.http.get_mapping(uri="admin/role/list", json_clazz=RoleList)
    @cjen.operate.asserts.validation_meta(meta_name="role_list", fields="procCode")
    def api_role_list(self, role_list: RoleList = None, resp=None, **kwargs):
        from eclinical.standard.steps.portal.user.portal_find_user_role import PortalFindUserRole
        self.step_definitions.call_back(PortalFindUserRole.Name, role_list=role_list)

    @cjen.http.put_mapping(uri="admin/role/{user_id}/user_group_role_rel", json_clazz=OkResponse)
    @cjen.operate.asserts.validation_meta(meta_name="ok", fields="procCode")
    def api_append_user_group_role_rel(self, path_variable, data, ok: OkResponse = None, resp=None, **kwargs):
        ...

    @cjen.http.get_mapping(uri="admin/user/{user_id}/user_group_role_rel", json_clazz=UserGroupRoleRel)
    @cjen.operate.asserts.validation_meta(meta_name="rel", fields="procCode")
    def api_user_group_role_rel(self, path_variable, rel: UserGroupRoleRel, resp=None, **kwargs):
        from eclinical.standard.steps.portal.user.portal_associated_usergroup import PortalAssociatedUserGroup
        self.step_definitions.call_back(PortalAssociatedUserGroup.Name, rel=rel)

    @cjen.http.post_mapping(uri="admin/user/query?pageNo={pageNo}&pageSize=25", json_clazz=Users)
    def api_user_query(self, path_variable, users: Users = None, resp=None, **kwargs):
        from eclinical.standard.steps.portal.user.portal_find_user import PortalFindUser
        self.step_definitions.call_back(PortalFindUser.Name, users=users)
        if not self.context[PortalFindUser.Id]:
            if not users.nextPage() == 0:
                self.api_user_query(path_variable=dict(pageNo=users.nextPage()))

    @cjen.http.post_mapping(uri="admin/user", json_clazz=OkResponse)
    @cjen.operate.asserts.validation_meta(meta_name="ok", fields="procCode")
    def api_create_user(self, data, ok: OkResponse, resp=None, **kwargs):
        ...

    @cjen.http.post_mapping(uri="admin/userGroup/query?pageNo={pageNo}&pageSize=25", json_clazz=QueryUserGroups)
    def get_user_group(self, path_variable, query: QueryUserGroups = None, resp=None, **kwargs):
        from eclinical.standard.steps.portal.user_groups.portal_find_usergroup import PortalFindUserGroup
        self.step_definitions.call_back(PortalFindUserGroup.Name, query=query)
        if not self.context[PortalFindUserGroup.Id]:
            if not query.nextPage() == 0:
                self.get_user_group(path_variable=dict(pageNo=query.nextPage()))
