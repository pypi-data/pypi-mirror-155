import cjen
from cjen import MetaJson


class RelUser(MetaJson):

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.userGroupName")
    def userGroupName(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.userGroupUserRelId")
    def userGroupUserRelId(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.userId")
    def userId(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.loginName")
    def loginName(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.firstName")
    def firstName(self): ...


class RoleRelUsers(MetaJson):

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.payload.nextPage")
    def nextPage(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.listOf(clazz=RelUser)
    @cjen.operate.json.one(json_path="$.payload.list")
    def list(self) -> list[RelUser]: ...

    @cjen.operate.asserts.equal(value=200)
    @cjen.operate.json.one(json_path="$.procCode")
    def procCode(self): ...
