from cjen.sco.standard_step import StandardStep

from eclinical.standard.portal.role import Role
from eclinical.standard.scenarios.portal_scenario import PortalScenario
from eclinical.standard.steps.portal.role.portal_find_role import PortalFindRole


class PortalCreateRole(StandardStep):
    Name = "portal_create_role.py"

    def __init__(self, service: Role, scenario: PortalScenario):
        self.service = service
        self.scenario = scenario
        self.service.step_definitions[self.Name] = self

    def _pre_processor(self):
        PortalFindRole(self.service, self.scenario).run()

    def ignore(self): return self.service.context[PortalFindRole.Id] is not None

    def category(self): return self.scenario.role().split("/")[0]

    def code(self): return self.scenario.role()

    def subCode(self): return self.scenario.role().split("/")[1]

    def data(self):
        return dict(category=self.category(), code=self.code(), subCode=self.subCode(), description="Test", active=True)

    def _execute(self): self.service.api_create_role(data=self.data())
