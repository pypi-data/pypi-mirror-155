from cjen.sco.scenario import Scenario
from cjen.sco.standard_step import StandardStep

from eclinical.standard.portal.hierarchies import Hierarchies
from eclinical.standard.scenarios.portal_scenario import PortalScenario
from eclinical.standard.steps.portal.hierarchies.portal_find_sponsor import PortalFindSponsor
from eclinical.standard.steps.portal.hierarchies.portal_sponsor_no_start import PortalSponsorNoStart


class PortalStartSponsor(StandardStep):
    Name = "portal_startup_sponsor.py"

    def __init__(self, service: Hierarchies, scenario: PortalScenario):
        self.service = service
        self.scenario = scenario
        self.service.step_definitions[self.Name] = self

    def _pre_processor(self):
        PortalFindSponsor(self.service, self.scenario).run()
        PortalSponsorNoStart(self.service, self.scenario).run()

    def ignore(self):
        return not self.service.context[PortalSponsorNoStart.System]

    def _execute(self):
        self.service.sponsor_startup(
            data=self.data(),
            path_variable=self.path_variable())

    def life_cycle(self): return self.scenario.life_cycle()

    def data(self): return self.service.context[PortalSponsorNoStart.System]

    def path_variable(self):
        return dict(sponsor_id=self.service.context[PortalFindSponsor.Id],
                    env_id=self.service.context[self.life_cycle()])
