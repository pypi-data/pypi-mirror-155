
from cjen.sco.standard_step import StandardStep

from eclinical.standard.portal.hierarchies import Hierarchies
from eclinical.standard.scenarios.portal_scenario import PortalScenario
from eclinical.standard.steps.portal.hierarchies.portal_find_sponsor import PortalFindSponsor
from eclinical.standard.steps.portal.hierarchies.portal_find_study import PortalFindStudy


class PortalCreateStudy(StandardStep):
    Name = "portal_create_study"

    def __init__(self, service: Hierarchies, scenario: PortalScenario):
        self.service = service
        self.scenario = scenario
        self.service.step_definitions[self.Name] = self

    def _pre_processor(self):
        PortalFindSponsor(self.service, self.scenario).run()

    def ignore(self):
        PortalFindStudy(self.service, self.scenario).run()
        return self.service.context[PortalFindStudy.Id] is not None

    def _execute(self):
        self.service.new_study(data=self.data())

    def study(self): return self.scenario.study()

    def sponsor(self): return self.scenario.sponsor()

    def data(self):
        return dict(active=True, description="", name=self.study(),
                    sponsorId=self.service.context[PortalFindSponsor.Id],
                    subjectManagement=5)
