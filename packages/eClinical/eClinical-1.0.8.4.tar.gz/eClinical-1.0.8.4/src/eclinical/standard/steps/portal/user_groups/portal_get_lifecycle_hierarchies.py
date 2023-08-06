from cjen.sco.scenario import Scenario
from cjen.sco.standard_step import StandardStep

from eclinical.standard.portal.dto.hierarchies.node import Node
from eclinical.standard.portal.dto.hierarchies.sponsor import Sponsor
from eclinical.standard.portal.user_groups import UserGroups
from eclinical.standard.scenarios.portal_scenario import PortalScenario
from eclinical.standard.steps.portal.hierarchies.portal_find_sponsor import PortalFindSponsor
from eclinical.standard.steps.portal.user_groups.portal_find_usergroup import PortalFindUserGroup
from eclinical.standard.steps.portal.user_groups.portal_get_company_envs import PortalGetCompanyEnvs


class PortalGetLifeCycleHierarchies(StandardStep):
    Name = "portal_get_lifecycle_hierarchies.py"
    Tree = "hierarchies"

    def __init__(self, service: UserGroups, scenario: PortalScenario):
        self.service = service
        self.scenario = scenario
        self.service.step_definitions[self.Name] = self

    def _pre_processor(self):
        PortalGetCompanyEnvs(self.service, self.scenario).run()

    def life_cycle(self):
        return self.scenario.life_cycle()

    def user_group(self):
        return self.scenario.user_group()

    def path_variable(self):
        for life_cycle in self.service.context[PortalGetCompanyEnvs.Object]:
            for life_cycle_name, life_cycle_id in life_cycle.items():
                if life_cycle_name == self.life_cycle():
                    return {"life_cycle_id": life_cycle_id, "userGroup_id": self.service.context[PortalFindUserGroup.Id]}
        return {"life_cycle_id": None}

    def call_back(self, **kwargs):
        self.service.context[self.Tree] = Sponsor.trees(kwargs.get("hierarchies").sponsorExtDtoList(),
                                                        self.service.context[PortalFindUserGroup.Id])

    def _execute(self):
        self.service.api_get_lifecycle_hierarchies(path_variable=self.path_variable())
