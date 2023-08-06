'''
Author: your name
Date: 2022-03-03 17:20:13
LastEditTime: 2022-03-03 17:44:13
LastEditors: your name
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \eClinical4.0_testing\eClinical\service\etmf_login_service.py
'''
import cjen

from eclinical.environment.environment import Environment
from eclinical.service._sponsor_login_service import _SponsorLoginService


class ETMFLoginService(_SponsorLoginService):
    @cjen.context.add(content=dict(system="eTMF"))
    def __init__(self, environment: Environment = None):
        super().__init__(environment)
        self.sponsor_auth()

    @cjen.http.post_mapping(uri="etmf/auth")
    @cjen.jwt(key="Authorization", json_path="$.payload.jwtAuthenticationResponse.token")
    def sponsor_auth(self, resp=None, **kwargs):
        ...
