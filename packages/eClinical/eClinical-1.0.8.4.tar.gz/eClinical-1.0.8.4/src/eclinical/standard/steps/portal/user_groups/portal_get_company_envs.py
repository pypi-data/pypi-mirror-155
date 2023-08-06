from cjen.sco.scenario import Scenario
from cjen.sco.standard_step import StandardStep

from eclinical.standard.portal.user_groups import UserGroups
from eclinical.standard.scenarios.portal_scenario import PortalScenario


class PortalGetCompanyEnvs(StandardStep):
    Name = "portal_get_company_envs"
    Id = "envIds"
    Object = "envObjects"

    def __init__(self, service: UserGroups, scenario: PortalScenario):
        self.service = service
        self.scenario = scenario
        self.service.step_definitions[self.Name] = self

    def _pre_processor(self): ...

    def call_back(self, **kwargs):
        self.service.context["envIds"] = [company_env.id() for company_env in kwargs.get("company_envs").list()]
        self.service.context[self.Object] = [{f'{company_env.name()}': company_env.id()} for company_env in
                                              kwargs.get("company_envs").list()]

    def _execute(self): self.service.api_company_envs()
