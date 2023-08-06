import cjen
from cjen import MetaJson


class CompanyMultipleEnv(MetaJson):

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.defaultEnv")
    def defaultEnv(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.companyId")
    def companyId(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.alias")
    def alias(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.name")
    def name(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.id")
    def id(self): ...


class UserGroupInfo(MetaJson):

    @cjen.operate.common.value
    @cjen.operate.json.listOf(clazz=CompanyMultipleEnv)
    @cjen.operate.json.one(json_path="$.payload.companyMultipleEnvs")
    def company_multiple_envs(self) -> list[CompanyMultipleEnv]: ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.id")
    def id(self): ...

    @cjen.operate.asserts.equal(value=200)
    @cjen.operate.json.one(json_path="$.procCode")
    def procCode(self): ...
