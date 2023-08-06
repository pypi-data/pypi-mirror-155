from cjen.sco.standard_step import StandardStep

from eclinical.standard.portal.user import User
from eclinical.standard.scenarios.portal_scenario import PortalScenario


class PortalFindUser(StandardStep):
    Name = "portal_find_user.py"
    Id = "user_id"

    def __init__(self, service: User, scenario: PortalScenario):
        self.service = service
        self.scenario = scenario
        self.service.step_definitions[self.Name] = self

    def user_name(self):
        return self.scenario.user().upper()

    def call_back(self, **kwargs):
        self.service.context[self.Id] = None
        for user in kwargs.get("users").list():
            if user.loginName() == self.user_name():
                self.service.context[self.Id] = user.id()

    def _execute(self):
        self.service.api_user_query(path_variable=dict(pageNo=1))
