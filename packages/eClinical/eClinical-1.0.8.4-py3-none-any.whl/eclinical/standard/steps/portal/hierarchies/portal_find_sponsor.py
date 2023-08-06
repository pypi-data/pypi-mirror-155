from cjen.sco.scenario import Scenario
from cjen.sco.standard_step import StandardStep

from eclinical.standard.portal.hierarchies import Hierarchies
from eclinical.standard.scenarios.portal_scenario import PortalScenario
from eclinical.standard.steps.portal.user_groups.portal_life_cycle import PortalLifeCycle


class PortalFindSponsor(StandardStep):
    Name = "portal_find_sponsor"
    Id = "sponsor_id"

    def __init__(self, service: Hierarchies, scenario: PortalScenario):
        self.service = service
        self.scenario = scenario
        self.service.step_definitions[self.Name] = self

    def sponsor(self):
        return self.scenario.sponsor()

    def _pre_processor(self):
        PortalLifeCycle(self.service, self.scenario).run()

    def _execute(self):
        self.service.get_sponsor(name=self.sponsor(), path_variable=self.path_variable())

    def call_back(self, **kwargs):
        self.service.context[self.Id] = None
        for sponsor in kwargs.get("query").sponsorExtDtoList():
            if sponsor.name() == self.sponsor():
                self.service.context[self.Id] = sponsor.id()

    def life_cycle(self):
        return self.scenario.life_cycle()

    def path_variable(self):
        return dict(env_id=self.service.context[self.life_cycle()])
