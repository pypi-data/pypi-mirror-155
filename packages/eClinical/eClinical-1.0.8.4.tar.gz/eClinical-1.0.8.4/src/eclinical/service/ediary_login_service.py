import cjen
from cjen import BigTangerine

import eclinical


class EDiaryLoginService(BigTangerine):
    @cjen.headers.basicHeaders(headers={
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json"
    })
    def __init__(self, environment: eclinical.Environment):
        super().__init__()
        self.environment = environment
        self.base_url = self.__dict__.get("base_url", self.environment.uri)
        self.context["userName"] = self.context.get("userName") or self.environment.user
        self.context["password"] = self.context.get("password") or self.environment.password
        self.edc_auth()
        self.edc_auth()

    @cjen.http.post_mapping(uri="admin/auth/subject/login")
    @cjen.jwt(key="Authorization", json_path="$.payload.jwtAuthenticationResponse.token")
    def auth(self, path_variable, data, resp=None, **kwargs): ...

    @cjen.http.post_mapping(uri="edc/subject/auth/login")
    @cjen.jwt(key="Authorization", json_path="$.payload.jwtAuthenticationResponse.token")
    def edc_auth(self, resp=None, **kwargs): ...
