import cjen

from eclinical.environment.environment import Environment
from eclinical.service._study_login_service import _StudyLoginService


class EdcLoginService(_StudyLoginService):
    @cjen.context.add(content=dict(system="EDC"))
    def __init__(self, environment: Environment = None):
        super().__init__(environment)
        self.study_auth()

    @cjen.http.post_mapping(uri="edc/auth")
    @cjen.jwt(key="Authorization", json_path="$.payload.jwtAuthenticationResponse.token")
    def study_auth(self, resp=None, **kwargs):
        ...