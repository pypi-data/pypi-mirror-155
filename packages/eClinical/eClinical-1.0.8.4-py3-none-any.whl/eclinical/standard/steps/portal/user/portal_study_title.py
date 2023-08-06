from cjen.sco.standard_step import StandardStep

from eclinical.standard.portal.user import User
from eclinical.standard.scenarios.portal_scenario import PortalScenario
from eclinical.standard.steps.portal.user.portal_find_user import PortalFindUser
from eclinical.standard.steps.portal.user.portal_user_access import PortalUserAccess


class PortalStudyTitle(StandardStep):
    Name = "portal_study_title.py"

    def __init__(self, service: User, scenario: PortalScenario):
        self.service = service
        self.scenario = scenario
        self.service.step_definitions[self.Name] = self

    def _pre_processor(self): ...

    def path_variable(self):
        return dict(user_id=self.service.context[PortalFindUser.Id])

    def data(self):
        return [dict(studyId=study_id, title=f'Title Of {study_id}', userId=self.service.context[PortalFindUser.Id])
                for study_id in self.service.context[PortalUserAccess.StudiesId]]

    def _execute(self):
        self.service.api_study_title(path_variable=self.path_variable(), data=self.data())
