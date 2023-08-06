import cjen

from cjen import MetaJson


class App(MetaJson):
    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.id")
    def id(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.name")
    def name(self): ...


class Systems(MetaJson):

    @cjen.operate.asserts.equal(value=200)
    @cjen.operate.json.one(json_path="$.procCode")
    def procCode(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.listOf(clazz=App)
    @cjen.operate.json.many(json_path="$.payload[?(@.hasRelation==False)]")
    def no_rel_apps(self) -> list[App]: ...
