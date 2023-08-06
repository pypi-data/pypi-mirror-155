import cjen
import eclinical

from eclinical.service._login_service import _LoginService
from eclinical.service.data._study_login_data import _StudyLoginData


class _StudyLoginService(_LoginService):

    def __init__(self, environment: eclinical.Environment):
        super().__init__(environment)
        self.auth(data=self.user_pwd())
        self.__cross_user() or self.__normal_user()
        self.user_onboard(
            data={k: v for k, v in self.context.content.items() if
                  k in ["applicationId", "sponsorId", "studyId", "envId", "workForCompanyId"]})

    def __cross_user(self):
        if self.context.get("company"):
            self.company()
            self.applications_cross_user(path_variable=dict(company_id=self.context.get("company_id")))
            self.context["workForCompanyId"] = self.context.get("company_id")
            return True
        return False

    def __normal_user(self):
        self.applications()

    @cjen.http.get_mapping(uri='admin/user/onboard/applications')
    @cjen.operate.json.factory(clazz=_StudyLoginData)
    def applications(self, resp=None, meta: _StudyLoginData = None, **kwargs) -> str:
        self.__update_login_info(meta)

    @cjen.http.get_mapping(uri='admin/user/onboard/applications?companyId={company_id}')
    @cjen.operate.json.factory(clazz=_StudyLoginData)
    def applications_cross_user(self, path_variable, resp=None, meta: _StudyLoginData = None, **kwargs):
        self.__update_login_info(meta)

    @cjen.http.post_mapping(uri="admin/user/onboard")
    @cjen.jwt(key="Authorization", json_path="$.payload.token")
    def user_onboard(self, data, resp=None, **kwargs):
        ...

    def __update_login_info(self, meta: _StudyLoginData):
        self.context["applicationId"] = meta.systemId()
        self.context["sponsorId"] = meta.sponsor_id()
        self.context["studyId"] = meta.study_id()
        self.context["envId"] = meta.env_id()