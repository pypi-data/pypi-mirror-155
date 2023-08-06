
from cjen.sco.standard_step import StandardStep

from eclinical.standard.portal.user import User
from eclinical.standard.scenarios.portal_scenario import PortalScenario


class PortalFindUserRole(StandardStep):
    Name = "portal_role_list.py"
    Id = "user_role_id"

    def __init__(self, service: User, scenario: PortalScenario):
        self.service = service
        self.scenario = scenario
        self.service.step_definitions[self.Name] = self

    def role(self):
        return self.scenario.role()

    def _execute(self):
        self.service.api_role_list()

    def call_back(self, **kwargs):
        for r in kwargs.get("role_list").payload():
            if r.code() == self.role():
                self.service.context[PortalFindUserRole.Id] = r.id()


