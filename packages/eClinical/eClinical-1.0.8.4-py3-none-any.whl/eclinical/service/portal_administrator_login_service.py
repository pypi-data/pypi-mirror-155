import cjen

from eclinical.environment.environment import Environment
from eclinical.service._login_service import _LoginService


class PortalAdministratorLoginService(_LoginService):
    def __init__(self, environment: Environment):
        super().__init__(environment)
        self.auth(data=self.user_pwd())

    @cjen.http.post_mapping(uri="admin/administrator/auth")
    @cjen.jwt(key="Authorization", json_path="$.payload.jwtAuthenticationResponse.token")
    def auth(self, data, resp=None, **kwargs): ...