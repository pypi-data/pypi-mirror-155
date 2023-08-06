import cjen
from cjen import MetaJson


class _SponsorLoginData(MetaJson):

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.payload[?(@.systemName=='{system}')].systemId")
    def systemId(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.payload[?(@.systemName=='{system}')].onboardSponsorList[?(@.name=='{"
                                     "sponsor}')].sponsorId")
    def sponsor_id(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.payload[?(@.systemName=='{system}')].onboardSponsorList[?(@.name=='{"
                                     "sponsor}')].onboardEnvs[?("
                                     "@.name=='{env}')].id")
    def env_id(self): ...