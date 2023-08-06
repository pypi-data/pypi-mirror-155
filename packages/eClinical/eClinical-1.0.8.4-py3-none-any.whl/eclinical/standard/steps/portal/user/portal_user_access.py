from cjen.sco.standard_step import StandardStep

from eclinical.standard.portal.user import User
from eclinical.standard.scenarios.portal_scenario import PortalScenario
from eclinical.standard.steps.portal.user.portal_find_user import PortalFindUser


class PortalUserAccess(StandardStep):
    Name = "portal_user_access.py"
    StudiesId = "user_access_permission_studies_id"

    def __init__(self, service: User, scenario: PortalScenario):
        self.service = service
        self.scenario = scenario
        self.service.step_definitions[self.Name] = self

    def _pre_processor(self):
        PortalFindUser(self.service, self.scenario).run()

    def path_variable(self): return {"user_id": self.service.context[PortalFindUser.Id]}

    def _execute(self): self.service.api_user_access(path_variable=self.path_variable())

    def call_back(self, **kwargs):
        id_of_studies = set()
        for user_permission_dto in kwargs.get("user_access").userPermissionDtoList():
            id_of_studies.add(user_permission_dto.studyId())
        self.service.context[self.StudiesId] = list(id_of_studies)
