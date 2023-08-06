import cjen

from eclinical import PortalLoginService, Environment
from eclinical.standard.base.ok_response import OkResponse

from eclinical.standard.portal.dto.company_envs import CompanyEnvs
from eclinical.standard.portal.dto.group_user import GroupUsers
from eclinical.standard.portal.dto.hierarchy import Hierarchy
from eclinical.standard.portal.dto.query_user_groups import QueryUserGroups
from eclinical.standard.portal.dto.user_group_info import UserGroupInfo


class UserGroups(PortalLoginService):
    LifeCycleId = "life_cycle_id"
    UserGroupId = "userGroup_id"
    PageNo = "pageNo"

    def __init__(self, environment: Environment = None):
        super().__init__(environment)

    @cjen.http.put_mapping(uri="admin/company/env/{life_cycle_id}/user-group/{userGroup_id}/hierarchies",json_clazz=OkResponse)
    @cjen.operate.asserts.validation_meta(meta_name="ok", fields="procCode")
    def api_set_lifecycle_hierarchies(self, path_variable, data, ok: OkResponse = None, resp=None, **kwargs):
        ...

    @cjen.http.get_mapping(uri="admin/company/env/{life_cycle_id}/user-group/{userGroup_id}/hierarchies",
                           json_clazz=Hierarchy)
    def api_get_lifecycle_hierarchies(self, path_variable, hierarchies: Hierarchy, resp=None, **kwargs):
        from eclinical.standard.steps.portal.user_groups.portal_get_lifecycle_hierarchies import \
            PortalGetLifeCycleHierarchies
        self.step_definitions.call_back(PortalGetLifeCycleHierarchies.Name, hierarchies=hierarchies)

    @cjen.http.post_mapping(uri="admin/userGroup/query?pageNo={pageNo}&pageSize=25", json_clazz=QueryUserGroups)
    def get_user_group(self, path_variable, query: QueryUserGroups = None, resp=None, **kwargs):
        from eclinical.standard.steps.portal.user_groups.portal_find_usergroup import PortalFindUserGroup
        self.step_definitions.call_back(PortalFindUserGroup.Name, query=query)
        if not self.context[PortalFindUserGroup.Id]:
            if not query.nextPage() == 0:
                self.get_user_group(path_variable=dict(pageNo=query.nextPage()))

    @cjen.http.get_mapping(uri="admin/userGroup/{userGroup_id}", json_clazz=UserGroupInfo)
    def user_group_info(self, path_variable, query: UserGroupInfo = None, resp=None, **kwargs):
        from eclinical.standard.steps.portal.user_groups.portal_get_user_group_info import PortalGetUserGroupInfo
        self.step_definitions.call_back(PortalGetUserGroupInfo.Name, query=query)

    @cjen.http.post_mapping(uri="admin/userGroup", json_clazz=OkResponse)
    @cjen.operate.asserts.validation_meta(meta_name="ok", fields="procCode")
    def create_user_group(self, data, ok: OkResponse = None, resp=None, **kwargs):
        from eclinical.standard.steps.portal.user_groups.portal_create_usergroup import PortalCreateUserGroup
        self.step_definitions.call_back(PortalCreateUserGroup.Name)

    @cjen.http.post_mapping(uri="admin/user")
    def create_user(self, data, resp=None, **kwargs):
        ...

    @cjen.http.get_mapping(uri="admin/company/envs", json_clazz=CompanyEnvs)
    def api_company_envs(self, company_envs: CompanyEnvs = None, resp=None, **kwargs):
        from eclinical.standard.steps.portal.user_groups.portal_get_company_envs import PortalGetCompanyEnvs
        self.step_definitions.call_back(PortalGetCompanyEnvs.Name, company_envs=company_envs)

    @cjen.http.post_mapping(uri="admin/userGroup/{userGroup_id}/unAddedUsers?pageNo=1&pageSize=25",
                            json_clazz=GroupUsers)
    def api_get_un_added_user(self, path_variable, group_users: GroupUsers = None, resp=None, **kwargs):
        from eclinical.standard.steps.portal.user_groups.portal_find_un_added_user import PortalFindUnAddedUser
        self.step_definitions.call_back(PortalFindUnAddedUser.Name, group_users=group_users)
        if not self.context["user_group_id"]:
            if not group_users.nextPage() == 0:
                self.get_user_group(path_variable=dict(pageNo=group_users.nextPage()))

    @cjen.http.post_mapping(uri="admin/userGroup/{userGroup_id}/add/users", json_clazz=OkResponse)
    @cjen.operate.asserts.validation_meta(meta_name="ok", fields="procCode")
    def api_add_group_user(self, path_variable, data, ok: OkResponse = None, resp=None, **kwargs):
        ...


if __name__ == '__main__':
    ug = UserGroups(
        environment=Environment(envir="DEV_01", file_path="D:\\github\\eclinical\\eclinical\\environment.yaml"))
    ug.api_un_added_user(path_variable=dict(userGroup_id=205))
    ug.api_add_group_user(path_variable=dict(userGroup_id=205), data=[{"userGroupId": 205, "userId": 2280}])
    # ug.create_user_group(data={"code": "UserGroup2", "active": True, "envIds": [105, 106, 107]})
    # ug.create_user_group(data={"code": "UserGroup3", "active": True, "envIds": [105, 106, 107]})
