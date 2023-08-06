import cjen
from cjen import MetaJson


class RelObject(MetaJson):

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.userId")
    def userId(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.userGroupUserRelId")
    def userGroupUserRelId(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.roleUserGroupUserRelId")
    def roleUserGroupUserRelId(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.userGroupId")
    def userGroupId(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.roleId")
    def roleId(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.id")
    def id(self): ...


class UserGroupRoleRel(MetaJson):

    @cjen.operate.common.value
    @cjen.operate.json.listOf(clazz=RelObject)
    @cjen.operate.json.one(json_path="$.payload")
    def list(self) -> list[RelObject]: ...

    @cjen.operate.asserts.equal(value=200)
    @cjen.operate.json.one(json_path="$.procCode")
    def procCode(self): ...
