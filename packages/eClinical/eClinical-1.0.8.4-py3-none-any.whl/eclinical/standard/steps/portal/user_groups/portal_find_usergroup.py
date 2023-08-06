from cjen.sco.scenario import Scenario
from cjen.sco.standard_step import StandardStep

from eclinical.standard.portal.user_groups import UserGroups
from eclinical.standard.scenarios.portal_scenario import PortalScenario


class PortalFindUserGroup(StandardStep):
    Name = "portal_find_user_group"
    Id = "user_group_id"

    def __init__(self, service: UserGroups, scenario: PortalScenario):
        self.service = service
        self.scenario = scenario
        self.service.step_definitions[self.Name] = self

    def user_group(self):
        return self.scenario.user_group()

    def call_back(self, **kwargs):
        self.service.context[self.Id] = None
        for user_group in kwargs.get("query").user_groups():
            if user_group.code() == self.user_group():
                self.service.context[self.Id] = user_group.id()

    def _execute(self):
        self.service.get_user_group(path_variable=dict(pageNo=1))
