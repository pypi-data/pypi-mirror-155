import cjen
from cjen import MetaJson


class UserRole(MetaJson):

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.id")
    def id(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.code")
    def code(self): ...


class UserRoles(MetaJson):
    
    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.payload.nextPage")
    def nextPage(self): ...
    
    @cjen.operate.common.value
    @cjen.operate.json.listOf(clazz=UserRole)
    @cjen.operate.json.one(json_path="$.payload")
    def list(self) -> list[UserRole]: ...
    
    @cjen.operate.asserts.equal(value=200)
    @cjen.operate.json.one(json_path="$.procCode")
    def procCode(self): ...
