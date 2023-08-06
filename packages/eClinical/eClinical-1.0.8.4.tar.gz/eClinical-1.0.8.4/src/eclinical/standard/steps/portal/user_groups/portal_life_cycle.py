from cjen.sco.scenario import Scenario
from cjen.sco.standard_step import StandardStep

from eclinical.standard.portal.hierarchies import Hierarchies
from eclinical.standard.scenarios.portal_scenario import PortalScenario


class PortalLifeCycle(StandardStep):
    Name = "portal_life_cycle"

    def __init__(self, service: Hierarchies, scenario: PortalScenario):
        self.service = service
        self.scenario = scenario
        self.service.step_definitions[self.Name] = self

    def call_back(self, **kwargs):
        for env in kwargs.get("envs").payload():
            if env.name() == self.life_cycle():
                self.service.context[self.life_cycle()] = env.id()

    def life_cycle(self):
        return self.scenario.life_cycle()

    def _execute(self):
        self.service.get_env_list(life_cycle=self.life_cycle())
