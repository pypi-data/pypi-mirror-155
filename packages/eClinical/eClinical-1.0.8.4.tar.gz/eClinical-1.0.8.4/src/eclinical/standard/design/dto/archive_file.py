import cjen
from cjen import MetaJson


class ArchiveFiles(MetaJson):

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.payload[?(@.id == 7)]")
    def db_spec(self): ...

    @cjen.operate.asserts.equal(value=200)
    @cjen.operate.json.one(json_path="$.procCode")
    def procCode(self): ...
