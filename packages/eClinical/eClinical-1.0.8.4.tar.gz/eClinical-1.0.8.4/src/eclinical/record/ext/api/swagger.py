import json
import os.path

import cjen
import re


class Swagger(cjen.BigTangerine):
    INIT = 1
    GET = 2

    def __init__(self):
        self.__setattr__("base_url", "http://52.82.79.202:81/")
        super().__init__()

    @cjen.http.get_mapping(uri="api/{system}/v2/api-docs")
    def doc(self, path_variable, resp=None, **kwargs):
        with open(os.path.join(os.path.curdir, f'swagger_{path_variable.get("system")}.json'), "w") as f:
            f.write(json.dumps(resp.get("paths")))

    @classmethod
    def with_param(cls, key):
        if re.findall(r'{([^}]+)}', key):
            return True
        return False

    def apis(self, system, action=GET):
        if not os.path.exists(os.path.join(os.path.curdir, f'swagger_{system}.json')):
            self.doc(path_variable=dict(system=system))
        if action == self.GET:
            with open(os.path.join(os.path.curdir, f'swagger_{system}.json'), "r") as f:
                try:
                    apis = json.loads(f.read()).keys()
                    apis = list(filter(self.with_param, apis))
                    return (key for key in apis)
                except Exception as e:
                    return []


if __name__ == '__main__':
    print(Swagger().apis("design"))
