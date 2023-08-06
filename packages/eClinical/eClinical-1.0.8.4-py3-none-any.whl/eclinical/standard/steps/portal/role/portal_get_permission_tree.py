from cjen.sco.standard_step import StandardStep

from eclinical.standard.portal.role import Role
from eclinical.standard.scenarios.portal_scenario import PortalScenario
from eclinical.standard.steps.portal.role.portal_find_role import PortalFindRole


class PortalGetPermissionTree(StandardStep):
    Name = "portal_get_permission_tree.py"
    IdOfAllPermission = "all_permissions_ids"

    def __init__(self, service: Role, scenario: PortalScenario):
        self.service = service
        self.scenario = scenario
        self.service.step_definitions[self.Name] = self

    def _pre_processor(self):
        PortalFindRole(self.service, self.scenario).run()

    def path_variable(self):
        return dict(role_id=self.service.context[PortalFindRole.Id])

    def _execute(self):
        self.service.api_all_permission_tree(path_variable=self.path_variable())

    def call_back(self, **kwargs):
        ids = set()
        for system in kwargs.get("pt").systems():
            self.get_permission_id(system, ids)
        self.service.context[self.IdOfAllPermission] = list(ids)

    def get_permission_id(self, node, cache):
        for menu in node.get("children"):
            cache.add(menu.get("id"))
            if menu.get("children"):
                self.get_permission_id(menu, cache)
