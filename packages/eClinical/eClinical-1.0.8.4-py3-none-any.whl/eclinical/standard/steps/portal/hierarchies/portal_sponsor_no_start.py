from cjen.exceptions import JsonPathNotFoundErr
from cjen.sco.standard_step import StandardStep

from eclinical.standard.portal.hierarchies import Hierarchies
from eclinical.standard.scenarios.portal_scenario import PortalScenario
from eclinical.standard.steps.portal.hierarchies.portal_find_sponsor import PortalFindSponsor


class PortalSponsorNoStart(StandardStep):
    Name = "portal_sponsor_no_start.py"
    System = "not_startup_sponsor"

    def __init__(self, service: Hierarchies, scenario: PortalScenario):
        self.service = service
        self.scenario = scenario
        self.service.step_definitions[self.Name] = self

    def _pre_processor(self):
        if not self.service.context[PortalFindSponsor.Id]:
            PortalFindSponsor(self.service, self.scenario).run()

    def _execute(self):
        self.service.sponsor_systems(path_variable=self.path_variable())

    def life_cycle(self):
        return self.scenario.life_cycle()

    def call_back(self, **kwargs):
        try:
            self.service.context[self.System] = [app.id() for app in kwargs.get("systems").no_rel_apps()]
        except JsonPathNotFoundErr as je:
            self.service.context[self.System] = None

    def path_variable(self):
        return dict(sponsor_id=self.service.context[PortalFindSponsor.Id], env_id=self.service.context[self.life_cycle()])
