import cjen
from cjen import MetaJson


class Role(MetaJson):
    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.active")
    def active(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.code")
    def code(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.id")
    def id(self): ...


class RoleList(MetaJson):

    @cjen.operate.common.value
    @cjen.operate.json.listOf(clazz=Role)
    @cjen.operate.json.one(json_path="$.payload.list")
    def all(self) -> list[Role]: ...

    @cjen.operate.common.value
    @cjen.operate.json.listOf(clazz=Role)
    @cjen.operate.json.one(json_path="$.payload")
    def payload(self) -> list[Role]: ...

    @cjen.operate.asserts.equal(value=200)
    @cjen.operate.json.one(json_path="$.procCode")
    def procCode(self): ...
