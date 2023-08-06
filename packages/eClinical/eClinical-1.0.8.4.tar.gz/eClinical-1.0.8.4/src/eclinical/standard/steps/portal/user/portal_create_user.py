from cjen.sco.scenario import Scenario
from cjen.sco.standard_step import StandardStep

from eclinical.standard.portal.user import User
from eclinical.standard.scenarios.portal_scenario import PortalScenario
from eclinical.standard.steps.portal.user.portal_find_user import PortalFindUser


class PortalCreateUser(StandardStep):
    Name = "portal_create_user.py"

    def __init__(self, service: User, scenario: PortalScenario):
        self.service = service
        self.scenario = scenario
        self.service.step_definitions[self.Name] = self

    def _pre_processor(self): PortalFindUser(self.service, self.scenario).run()

    def ignore(self):
        return self.service.context[PortalFindUser.Id] is not None

    def login_name(self): return self.scenario.user()

    def pass_word(self): return self.service.encypt_password("Admin@123")

    def data(self):
        return {
            "firstName": self.login_name()[0],
            "lastName": self.login_name()[1:],
            "loginName": self.login_name(),
            "password": self.pass_word(),
            "phoneNumber": "88888888",
            "email": f'{self.login_name()}@163.com', "active": True, "etmfAdministrator": False}

    def _execute(self): self.service.api_create_user(data=self.data())
