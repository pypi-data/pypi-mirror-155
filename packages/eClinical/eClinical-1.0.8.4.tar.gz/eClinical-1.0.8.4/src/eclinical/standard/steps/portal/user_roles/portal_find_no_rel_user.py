from cjen.sco.scenario import Scenario
from cjen.sco.standard_step import StandardStep

from eclinical.standard.portal.user_role import UserRole
from eclinical.standard.scenarios.portal_scenario import PortalScenario
from eclinical.standard.steps.portal.user_roles.portal_get_user_role import PortalGetUserRole


class PortalFindNoRelUser(StandardStep):
    Name = "portal_find_no_rel_user.py"

    def __init__(self, service: UserRole, scenario: PortalScenario):
        self.service = service
        self.scenario = scenario
        self.service.step_definitions[self.Name] = self

    def _pre_processor(self):
        PortalGetUserRole(self.service, self.scenario).run()

    def path_variable(self):
        return dict(role_id=self.service.context[PortalGetUserRole.Id])

    def _execute(self):
        self.service.get_no_relations_users(path_variable=self.path_variable())
