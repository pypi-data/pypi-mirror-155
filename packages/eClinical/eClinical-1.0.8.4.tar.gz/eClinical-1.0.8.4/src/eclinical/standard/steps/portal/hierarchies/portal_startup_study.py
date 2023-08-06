
from cjen.sco.standard_step import StandardStep

from eclinical.standard.portal.hierarchies import Hierarchies
from eclinical.standard.scenarios.portal_scenario import PortalScenario
from eclinical.standard.steps.portal.hierarchies.portal_find_study import PortalFindStudy
from eclinical.standard.steps.portal.hierarchies.portal_study_no_start import PortalStudyNoStart


class PortalStartupStudy(StandardStep):
    Name = "portal_startup_study"

    def __init__(self, service: Hierarchies, scenario: PortalScenario):
        self.service = service
        self.scenario = scenario
        self.service.step_definitions[self.Name] = self

    def _pre_processor(self):
        PortalFindStudy(self.service, self.scenario).run()
        PortalStudyNoStart(self.service, self.scenario).run()

    def ignore(self):
        return not self.service.context[PortalStudyNoStart.System]

    def _execute(self):
        self.service.study_startup(
            data=self.data(),
            path_variable=self.path_variable())

    def life_cycle(self): return self.scenario.life_cycle()

    def data(self): return self.service.context[PortalStudyNoStart.System]

    def path_variable(self):
        return dict(study_id=self.service.context[PortalFindStudy.Id],
                    env_id=self.service.context[self.life_cycle()])
