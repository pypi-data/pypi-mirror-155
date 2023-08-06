import cjen
from cjen import MetaJson


class VersionInfo(MetaJson):

    @cjen.operate.asserts.equal(value=200)
    @cjen.operate.json.one(json_path="$.procCode")
    def procCode(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(
        json_path="$.payload[?(@.isCurrent==True)]")
    def current_version(self): ...
