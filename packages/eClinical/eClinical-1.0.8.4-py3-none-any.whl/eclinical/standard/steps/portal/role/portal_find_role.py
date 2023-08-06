
from cjen.sco.standard_step import StandardStep

from eclinical.standard.portal.role import Role
from eclinical.standard.scenarios.portal_scenario import PortalScenario


class PortalFindRole(StandardStep):
    Name = "portal_find_role.py"
    Id = "role_id"

    def __init__(self, service: Role, scenario: PortalScenario):
        self.service = service
        self.scenario = scenario
        self.service.step_definitions[self.Name] = self

    def path_variable(self): return dict(pageNo=1)

    def role_name(self):
        return self.scenario.role()

    def call_back(self, **kwargs):
        self.service.context[self.Id] = None
        for role in kwargs.get("role_list").all():
            if role.code() == self.role_name():
                self.service.context[self.Id] = role.id()

    def _execute(self):
        self.service.api_query(path_variable=self.path_variable())
