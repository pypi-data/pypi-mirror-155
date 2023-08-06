import cjen
from cjen import MetaJson


class Study(MetaJson):

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.name")
    def name(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.id")
    def id(self): ...


class QueryStudies(MetaJson):

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.payload.nextPage")
    def nextPage(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.listOf(clazz=Study)
    @cjen.operate.json.one(json_path="$.payload.list")
    def studies(self) -> list[Study]: ...

    @cjen.operate.asserts.equal(value=200)
    @cjen.operate.json.one(json_path="$.procCode")
    def procCode(self): ...
