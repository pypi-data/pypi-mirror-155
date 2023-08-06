import cjen
from cjen import MetaJson


class User(MetaJson):
    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.companyId")
    def companyId(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.active")
    def active(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.loginName")
    def loginName(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.id")
    def id(self): ...


class Users(MetaJson):

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.payload.nextPage")
    def nextPage(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.listOf(clazz=User)
    @cjen.operate.json.one(json_path="$.payload.list")
    def list(self) -> list[User]: ...

    @cjen.operate.asserts.equal(value=200)
    @cjen.operate.json.one(json_path="$.procCode")
    def procCode(self): ...
