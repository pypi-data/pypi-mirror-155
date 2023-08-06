import re
from urllib.parse import urlparse, parse_qs, urlunparse

from eclinical.record.ext.api.swagger import Swagger


class ApiSpec:

    def __init__(self, resource, application):
        self.application = application
        self.apis = resource.apis(self.application)
        self.hava_data = False
        self.have_path_variable = False

    @classmethod
    def api(cls, resource, http):
        application = http.path.split("/")[2]
        return ApiSpec(resource, application).spec(http=http)

    def spec(self, http):
        # 只能识别 ID 的接口
        http_path = "/".join(http.path.split("/")[2:])
        return self.parameters_in_query(http_path) or self.parameters_in_path(http_path) or http_path

    def parameters_in_path(self, http_path):
        for api in self.apis:
            api_regex = re.sub(r'\{\w+[Id | id | ID]\}', '\\\d+', f'{self.application}{api}')
            api_regex = re.sub(r'\{env}', '\\\d+', api_regex)
            api_regex = re.sub(r'\{location\}', '\\\d+', api_regex)
            try:
                if re.match(api_regex, http_path):
                    self.have_path_variable = True
                    return f'{self.application}{api}'
            except Exception as e:
                continue
        return None

    def parameters_in_query(self, http_path):
        result = urlparse(http_path)
        if  result.query:
            query = "&".join([f'{key}={{{key}}}' for key in parse_qs(result.query).keys()])
            self.have_path_variable = True
            return urlunparse(["", "", result.path, result.params, query, result.fragment])
        return None


if __name__ == '__main__':
    # print(ApiSpec(Swagger(), "admin").spec("admin/user/onboard/applications?companyId=1"))
    result = urlparse("http://200.200.101.113/api")
    print(result.hostname)