import time

import cjen
import eclinical
import jsonpath
from cjen import BigTangerine

from eclinical.utils.ecrypto import Ecrypto


class _LoginService(BigTangerine):
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
        self.context["company"] = self.context.get('company') or self.environment.company
        self.context["sponsor"] = self.context.get("sponsor") or self.environment.sponsor
        self.context["study"] = self.context.get("study") or self.environment.study
        self.context["env"] = self.context.get("env") or self.environment.life_cycle

    @cjen.http.post_mapping(uri="admin/auth")
    @cjen.jwt(key="Authorization", json_path="$.payload.jwtAuthenticationResponse.token")
    def auth(self, data, resp=None, **kwargs): ...

    @cjen.http.get_mapping(uri="admin/user/onboard/company")
    def company(self, resp=None, **kwargs):
        self.context["company_id"] = \
            jsonpath.jsonpath(resp,
                              f"$.payload[?(@.name=='{self.context.get('company')}')].id")[
                0]

    def encypt_password(self, pwd):
        return Ecrypto(self.environment).en(repr(dict(password=pwd, time=int(time.time() * 1000))).replace("'", "\""))

    def user_pwd(self):
        return dict(userName=self.context.get("userName") or self.environment.user,
                    password=self.encypt_password(self.context.get("password") or self.environment.password))