from cjen.sco.scenario import Scenario
from cjen.sco.standard_step import StandardStep

from eclinical.standard.portal.user_groups import UserGroups
from eclinical.standard.scenarios.portal_scenario import PortalScenario
from eclinical.standard.steps.portal.user_groups.portal_find_usergroup import PortalFindUserGroup


class PortalFindUnAddedUser(StandardStep):
    Name = "portal_get_un_added_user.py"

    def __init__(self, service: UserGroups, scenario: PortalScenario):
        self.service = service
        self.scenario = scenario
        self.service.step_definitions[self.Name] = self

    def _pre_processor(self):
        PortalFindUserGroup(self.service, self.scenario).run()

    def call_back(self, **kwargs):
        self.service.context["user_id"] = None
        for user in kwargs.get("group_users").list():
            if user.loginName() == self.user_name():
                self.service.context["user_id"] = user.id()

    def _post_processor(self):
        print("user_id", self.service.context["user_id"])

    def user_name(self): return self.scenario.user()

    def _execute(self): self.service.api_get_un_added_user(path_variable=self.path_variable())

    def path_variable(self): return dict(userGroup_id=self.service.context["user_group_id"])
