import re

from swagger import Swagger


class ApiSpec:

    def __init__(self, resource):
        self.apis = resource.apis(self.system)

    @property
    def system(self):
        return ""

    @classmethod
    def name(cls, http_path: str, resource_clazz):
        resource = resource_clazz()
        for api_spec_clazz in ([DESIGN, EDC, PV, ADMIN, IWRS, eTMF,  CTMS]):
            api_spec = api_spec_clazz(resource)
            if api_spec.system == http_path.split("/")[0]:
                return api_spec.spec(http_path)
        raise  Exception("没有该系统")

    def spec(self, http_path):
        for api in self.apis:
            api_regex = re.sub(r'\{\w+[Id | id | ID]\}', '\\\d+', f'{self.system}{api}')
            api_regex = re.sub(r'\{env}', '\\\d+', api_regex)
            api_regex = re.sub(r'\{location\}', '\\\d+', api_regex)
            if re.match(api_regex, http_path):
                return f'{self.system}{api}'
        return http_path


class DESIGN(ApiSpec):
    @property
    def system(self): return "design"


class EDC(ApiSpec):
    @property
    def system(self): return "edc"


class IWRS(ApiSpec):
    @property
    def system(self): return "iwrs"


class PV(ApiSpec):
    @property
    def system(self): return "pv"


class ADMIN(ApiSpec):
    @property
    def system(self): return "admin"


class eTMF(ApiSpec):
    @property
    def system(self): return "etmf"


class CTMS(ApiSpec):
    @property
    def system(self): return "ctms"


if __name__ == '__main__':
    print(ApiSpec.name("design/study/12/switch", Swagger))
