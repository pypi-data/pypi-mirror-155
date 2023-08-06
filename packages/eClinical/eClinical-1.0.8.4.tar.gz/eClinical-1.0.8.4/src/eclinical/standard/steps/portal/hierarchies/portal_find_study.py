
from cjen.sco.standard_step import StandardStep

from eclinical.standard.portal.hierarchies import Hierarchies
from eclinical.standard.scenarios.portal_scenario import PortalScenario
from eclinical.standard.steps.portal.hierarchies.portal_find_sponsor import PortalFindSponsor


class PortalFindStudy(StandardStep):
    Name = "portal_find_study"
    Id = "study_id"

    def __init__(self, service: Hierarchies, scenario: PortalScenario):
        self.service = service
        self.scenario = scenario
        self.service.step_definitions[self.Name] = self

    def _pre_processor(self):
        PortalFindSponsor(self.service, self.scenario).run()

    def sponsor(self):
        return self.scenario.sponsor()

    def study(self):
        return self.scenario.study()

    def call_back(self, **kwargs):
        self.service.context[self.Id] = None
        for study in kwargs.get("query").studies():
            if study.name() == self.study():
                self.service.context[self.Id] = study.id()

    def _execute(self):
        self.service.get_study(
            data=self.data(),
            path_variable=self.path_variable())

    def data(self):
        return dict(sponsorId=self.service.context[PortalFindSponsor.Id])

    def path_variable(self):
        return dict(pageNo=1)
