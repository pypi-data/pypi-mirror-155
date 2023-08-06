import cjen
from cjen.sco.step_definitions import StepDefinitions

from eclinical import PortalLoginService, Environment
from eclinical.standard.base.ok_response import OkResponse
from eclinical.standard.portal.dto.permission_tree import PermissionTree
from eclinical.standard.portal.dto.role_list import RoleList


class Role(PortalLoginService):
    def __init__(self, environment: Environment = None):
        super().__init__(environment)
        self.step_definitions = StepDefinitions()
    
    @cjen.http.put_mapping(uri="admin/role/{role_id}/permissions",json_clazz=OkResponse)
    @cjen.operate.asserts.validation_meta(meta_name="ok", fields="procCode")
    def api_set_permissions(self, path_variable, data, ok: OkResponse = None, resp=None, **kwargs): ...
    
    @cjen.http.get_mapping(uri="admin/role/{role_id}/allPermissionTree", json_clazz=PermissionTree)
    def api_all_permission_tree(self, path_variable, pt: PermissionTree = None, resp=None, **kwargs):
        from eclinical.standard.steps.portal.role.portal_get_permission_tree import PortalGetPermissionTree
        self.step_definitions.call_back(PortalGetPermissionTree.Name, pt=pt)

    @cjen.http.post_mapping(uri="admin/role")
    def api_create_role(self, data, resp=None, **kwargs): ...

    @cjen.http.get_mapping(uri="admin/role/category/list", json_clazz=OkResponse)
    @cjen.operate.asserts.validation_meta(meta_name="ok", fields="procCode")
    def api_category_list(self, ok: OkResponse = None, resp=None, **kwargs): ...

    @cjen.http.post_mapping(uri="admin/role/query?pageNo={pageNo}&pageSize=25", json_clazz=RoleList)
    def api_query(self, path_variable, role_list: RoleList, resp=None, **kwargs):
        from eclinical.standard.steps.portal.role.portal_find_role import PortalFindRole
        self.step_definitions.call_back(PortalFindRole.Name, role_list=role_list)
