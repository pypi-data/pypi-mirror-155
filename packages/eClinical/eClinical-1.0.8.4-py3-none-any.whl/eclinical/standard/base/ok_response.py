import cjen
from cjen import MetaJson


class OkResponse(MetaJson):

    @cjen.operate.asserts.equal(value=200)
    @cjen.operate.json.one(json_path="$.procCode")
    def procCode(self): ...