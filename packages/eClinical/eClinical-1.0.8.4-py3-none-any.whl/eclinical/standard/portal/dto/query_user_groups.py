import cjen
from cjen import MetaJson


class UserGroup(MetaJson):
    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.code")
    def code(self): ...
    
    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.id")
    def id(self): ...
    

class QueryUserGroups(MetaJson):
    
    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.payload.nextPage")
    def nextPage(self): ...
    
    @cjen.operate.common.value
    @cjen.operate.json.listOf(clazz=UserGroup)
    @cjen.operate.json.one(json_path="$.payload.list")
    def user_groups(self) -> list[UserGroup]: ...

    @cjen.operate.asserts.equal(value=200)
    @cjen.operate.json.one(json_path="$.procCode")
    def procCode(self): ...
