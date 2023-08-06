

SPACE4 = "    "
class Service:
    def __init__(self, service_name, app):
        self.service_name = service_name
        self.app = app

    @property
    def file_name(self):
        return f"{self.service_name}_service"

    @property
    def clazz_name(self):
        return "".join([elem.capitalize() for elem in self.file_name.split("_")])

    @property
    def application(self):
        return self.app

    @property
    def application_clazz(self):
        clazz = dict(etmf="ETMFLoginService", pv="PVLoginService", ctms="CTMSLoginService", edc="EdcLoginService",
                     iwrs="IWRSLoginService", design="DesignLoginService", portal="PortalLoginService",
                     portaladmin="PortalAdministratorLoginService").get(self.application.lower(), "BigTangerine")
        return clazz

    @classmethod
    def output_conftest_header_py(cls):
        return "import pytest\n\n" + \
               "from environment.environment import Environment\n\n"

    def output_conftest_body_py(self):
        return f"from .services.{self.file_name} import {self.clazz_name}\n\n\n" + \
               f"@pytest.fixture\n" + f"def {self.file_name}(ef, st):\n" + \
               f"\treturn {self.clazz_name}(Environment(envir=st, file_path=ef))\n\n\n"

    def output_init_py(self):
        return f"from .{self.file_name} import {self.clazz_name}\n"

    def output_service_py(self):

        if self.application_clazz == "BigTangerine":
            import_str = "import cjen\n\nfrom cjen import BigTangerine,DatabasePool\nfrom eclinical import Environment\n\n\n"
            super_str = "        super().__init__()\n"
        else:
            import_str = f"import cjen\n\nfrom cjen import DatabasePool\nfrom eclinical import {self.application_clazz}, Environment\n\n\n"
            super_str = "        super().__init__(environment)\n"
        return import_str + \
               f"class {self.clazz_name}({self.application_clazz}):\n" + \
               "    \"\"\"\n    相关使用详情可查询:\n" \
               "    http 装饰器: https://github.com/thcpc/cjen#432-http-%E8%A3%85%E9%A5%B0%E5%99%A8\n" +\
               "    数据构造 装饰器: https://github.com/thcpc/cjen#433-factory-%E8%A3%85%E9%A5%B0%E5%99%A8\n " + \
               "    \"\"\"\n\n" + \
               f"    def __init__(self, environment: Environment):\n" + \
               super_str + \
               f"        self.context['cursor'] = DatabasePool.cursor(host=environment.db.get(\"host\"), user=environment.db.get(\"user\"), pwd=environment.db.get(\"pwd\"), port=environment.db.get(\"port\"), database=environment.db.get(\"database\"))\n\n"

    def _method_name(self, api_url): pass

    def _method_body(self, api_url, flow):
        return f'{SPACE4}def  {self._method_name(api_url)}({self._method_args(api_url,flow)}, resp=None, **kwargs): ...\n'

    def _decorator_http_name(self,flow): return "post_mapping"

    def _method_decorator(self, api_url, flow):
        return f'{SPACE4}@cjen.http.{self._decorator_http_name(flow)}(uri={api_url})'

    def _method_args(self, api_url, flow):
        if '{' in api_url and flow.request.body is not None: return "path_variable, data"
        if '{' in api_url: return "path_variable"
        if flow.request.body is not None: return "data"

    def output_method(self, api_url, flow):
        return f'{self._method_decorator(api_url, flow)}\n{self._method_body(api_url, flow)}\n'

        # annoation = f'    @cjen.http.post(uri={api_url})'
        # method = f'    def {}'