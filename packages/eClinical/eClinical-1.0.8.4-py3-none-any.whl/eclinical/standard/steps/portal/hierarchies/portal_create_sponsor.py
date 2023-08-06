from cjen.sco.standard_step import StandardStep

from eclinical.standard.portal.hierarchies import Hierarchies
from eclinical.standard.scenarios.portal_scenario import PortalScenario
from eclinical.standard.steps.portal.hierarchies.portal_find_sponsor import PortalFindSponsor


class PortalCreateSponsor(StandardStep):
    Name = "portal_create_sponsor.py"

    def __init__(self, service: Hierarchies, scenario: PortalScenario):
        self.service = service
        self.scenario = scenario
        self.service.step_definitions[self.Name] = self

    def _pre_processor(self):
        PortalFindSponsor(self.service, self.scenario).run()

    def ignore(self):
        return self.service.context["sponsor_id"] is not None

    def sponsor_name(self): return self.scenario.sponsor()

    def data(self):
        return {"name": self.sponsor_name(), "description": "", "active": True}

    def _execute(self): self.service.new_sponsor(data=self.data())
