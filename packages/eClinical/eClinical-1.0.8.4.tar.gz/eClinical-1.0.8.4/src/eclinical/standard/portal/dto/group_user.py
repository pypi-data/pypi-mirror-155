import cjen
from cjen import MetaJson


class GroupUser(MetaJson):

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.email")
    def email(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.id")
    def id(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.loginName")
    def loginName(self): ...


class GroupUsers(MetaJson):

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.payload.nextPage")
    def nextPage(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.listOf(clazz=GroupUser)
    @cjen.operate.json.one(json_path="$.payload.list")
    def list(self) -> list[GroupUser]: ...

    @cjen.operate.asserts.equal(value=200)
    @cjen.operate.json.one(json_path="$.procCode")
    def procCode(self): ...

