import cjen
import re


class Swagger(cjen.BigTangerine):
    def __init__(self):
        self.__setattr__("base_url", "http://52.82.79.202:81/")
        super().__init__()

    @cjen.http.get_mapping(uri="api/{system}/v2/api-docs")
    def doc(self, path_variable, resp=None, **kwargs):
        ...

    @classmethod
    def with_param(cls, key):
        if re.findall(r'{([^}]+)}', key):
            return True
        return False

    def apis(self, system):
        try:
            apis = list(filter(self.with_param, self.doc(path_variable=dict(system=system)).get("paths").keys()))
            return (key for key in apis)
        except Exception as e:
            return []


if __name__ == '__main__':
    print(Swagger().apis("design"))
