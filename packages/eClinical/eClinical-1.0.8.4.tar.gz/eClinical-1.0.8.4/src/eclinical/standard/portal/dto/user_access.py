import cjen
from cjen import MetaJson


class UserPermissionDto(MetaJson):

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.sponsorId")
    def sponsorId(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.studyId")
    def studyId(self): ...


class UserAccess(MetaJson):

    @cjen.operate.common.value
    @cjen.operate.json.listOf(clazz=UserPermissionDto)
    @cjen.operate.json.one(json_path="$.payload.userPermissionDtoList")
    def userPermissionDtoList(self) -> list[UserPermissionDto]: ...

    @cjen.operate.asserts.equal(value=200)
    @cjen.operate.json.one(json_path="$.procCode")
    def procCode(self): ...
