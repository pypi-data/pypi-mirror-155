import cjen
from cjen import MetaJson


class CompanyEnv(MetaJson):

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.defaultEnv")
    def defaultEnv(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.name")
    def name(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.id")
    def id(self): ...


class CompanyEnvs(MetaJson):

    @cjen.operate.common.value
    @cjen.operate.json.listOf(clazz=CompanyEnv)
    @cjen.operate.json.one(json_path="$.payload")
    def list(self) -> list[CompanyEnv]: ...

    @cjen.operate.asserts.equal(value=200)
    @cjen.operate.json.one(json_path="$.procCode")
    def procCode(self): ...
