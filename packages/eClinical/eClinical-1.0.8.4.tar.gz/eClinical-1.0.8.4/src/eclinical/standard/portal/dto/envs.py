import cjen

from cjen import MetaJson


class Env(MetaJson):

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.id")
    def id(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.name")
    def name(self): ...


class Envs(MetaJson):

    @cjen.operate.asserts.equal(value=200)
    @cjen.operate.json.one(json_path="$.procCode")
    def procCode(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.listOf(clazz=Env)
    @cjen.operate.json.one(json_path="$.payload")
    def payload(self) -> list[Env]: ...
