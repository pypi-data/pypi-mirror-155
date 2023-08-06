import cjen
from cjen import MetaJson


class SiteDto(MetaJson):
    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.hasRelation")
    def hasRelation(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.id")
    def id(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.code")
    def code(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.name")
    def name(self): ...


class StudyDto(MetaJson):
    @cjen.operate.common.value
    @cjen.operate.json.listOf(clazz=SiteDto)
    @cjen.operate.json.one(json_path="$.siteList")
    def siteList(self) -> list[SiteDto]: ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.hasRelation")
    def hasRelation(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.name")
    def name(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.id")
    def id(self): ...


class SponsorExtDto(MetaJson):
    @cjen.operate.common.value
    @cjen.operate.json.listOf(clazz=StudyDto)
    @cjen.operate.json.one(json_path="$.studyList")
    def studyList(self) -> list[StudyDto]: ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.hasRelation")
    def hasRelation(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.name")
    def name(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.id")
    def id(self): ...


class Hierarchy(MetaJson):

    @cjen.operate.common.value
    @cjen.operate.json.listOf(clazz=SponsorExtDto)
    @cjen.operate.json.one(json_path="$.payload.sponsorExtDtoList")
    def sponsorExtDtoList(self) -> list[SponsorExtDto]: ...

    @cjen.operate.asserts.equal(value=200)
    @cjen.operate.json.one(json_path="$.procCode")
    def procCode(self): ...
