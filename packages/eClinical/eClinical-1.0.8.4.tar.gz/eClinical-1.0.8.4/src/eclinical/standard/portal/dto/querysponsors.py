import cjen
from cjen import MetaJson


class Sponsor(MetaJson):
    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.name")
    def name(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.id")
    def id(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.active")
    def active(self): ...


class QuerySponsors(MetaJson):
    @cjen.operate.asserts.equal(value=200)
    @cjen.operate.json.one(json_path="$.procCode")
    def procCode(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.listOf(clazz=Sponsor)
    @cjen.operate.json.one(json_path="$.payload.sponsorExtDtoList")
    def sponsorExtDtoList(self) -> list[Sponsor]: ...


