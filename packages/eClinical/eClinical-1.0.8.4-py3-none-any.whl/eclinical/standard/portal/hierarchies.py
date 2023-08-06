import cjen
from cjen.sco.step_definitions import StepDefinitions

from eclinical import Environment
from eclinical.service.portal_login_service import PortalLoginService
from eclinical.standard.base.ok_response import OkResponse

from eclinical.standard.portal.dto.envs import Envs
from eclinical.standard.portal.dto.querysponsors import QuerySponsors
from eclinical.standard.portal.dto.query_studies import QueryStudies
from eclinical.standard.portal.dto.systems import Systems


class Hierarchies(PortalLoginService):
    def __init__(self, environment: Environment = None):
        super().__init__(environment)
        self.step_definitions = StepDefinitions()

    @cjen.http.get_mapping(uri="admin/company/envs", json_clazz=Envs)
    @cjen.operate.asserts.validation_meta(meta_name="envs")
    def get_env_list(self, envs: Envs = None, resp=None, **kwargs):
        from eclinical.standard.steps.portal.user_groups.portal_life_cycle import PortalLifeCycle
        self.step_definitions.call_back(PortalLifeCycle.Name, envs=envs)

    @cjen.http.get_mapping(uri="admin/company/env/{env_id}/hierarchies", json_clazz=QuerySponsors)
    @cjen.operate.asserts.validation_meta(meta_name="query")
    def get_sponsor(self, path_variable, query: QuerySponsors = None, resp=None, **kwargs):
        from eclinical.standard.steps.portal.hierarchies.portal_find_sponsor import PortalFindSponsor
        self.step_definitions.call_back(PortalFindSponsor.Name, query=query)

    @cjen.http.post_mapping(uri="admin/study/query?pageNo={pageNo}&pageSize=25", json_clazz=QueryStudies)
    def get_study(self, path_variable, data, query: QueryStudies = None, resp=None, **kwargs):
        from eclinical.standard.steps.portal.hierarchies.portal_find_study import PortalFindStudy
        self.context["study_id"] = None
        self.step_definitions.call_back(PortalFindStudy.Name, query=query)

        if not self.context["study_id"]:
            if not query.nextPage() == 0:
                self.get_study(path_variable=dict(pageNo=query.nextPage()), data=data)

    @cjen.http.post_mapping(uri="admin/sponsor", json_clazz=OkResponse)
    @cjen.operate.asserts.validation_meta(meta_name="ok")
    def new_sponsor(self, data, ok: OkResponse = None, resp=None, **kwargs):
        ...

    @cjen.http.post_mapping(uri="admin/study", json_clazz=OkResponse)
    @cjen.operate.asserts.validation_meta(meta_name="ok")
    def new_study(self, data, ok: OkResponse = None, resp=None, **kwargs):
        ...

    @cjen.http.get_mapping(uri="admin/sponsor/{sponsor_id}/env/{env_id}/systems", json_clazz=Systems)
    def sponsor_systems(self, path_variable, systems: Systems = None, resp=None, **kwargs):
        from eclinical.standard.steps.portal.hierarchies.portal_sponsor_no_start import PortalSponsorNoStart
        self.step_definitions.call_back(PortalSponsorNoStart.Name, systems=systems)

    @cjen.http.get_mapping(uri="admin/study/{study_id}/env/{env_id}/systems", json_clazz=Systems)
    def study_systems(self, path_variable, systems: Systems = None, resp=None, **kwargs):
        from eclinical.standard.steps.portal.hierarchies.portal_study_no_start import PortalStudyNoStart
        self.step_definitions.call_back(PortalStudyNoStart.Name, systems=systems)

    @cjen.http.post_mapping(uri="admin/study/{study_id}/env/{env_id}/database", json_clazz=OkResponse)
    @cjen.operate.asserts.validation_meta(meta_name="ok")
    def study_startup(self, path_variable, data, ok: OkResponse = None, resp=None, **kwargs):
        ...

    @cjen.http.post_mapping(uri="admin/sponsor/{sponsor_id}/env/{env_id}/database", json_clazz=OkResponse)
    @cjen.operate.asserts.validation_meta(meta_name="ok")
    def sponsor_startup(self, path_variable, data, ok: OkResponse = None, resp=None, **kwargs):
        ...

# if __name__ == '__main__':
#     cs = Hierarchies(
#         environment=Environment(envir="AWS_Test", file_path="D:\\github\\eclinical\\eclinical\\environment.yaml"))
#     cs.get_env_list(life_cycle="dev")
#     cs.get_sponsor(name="chenpengcheng", path_variable=dict(env_id=cs.context[cs.environment.life_cycle]), query=)
#     cs.get_study(name="CPC033", data=dict(sponsorId=cs.context[f'sponsor_chenpengcheng']), path_variable=dict(pageNo=1))
#     print(cs.context["study_id"])
# for i in range(2, 100):
#     cs.new_study(data=dict(active=True, description="", name=f'CPC0{i}',
#                            sponsorId=cs.context[f"sponsor_chenpengcheng"],
#                            subjectManagement=5))
# cs.system_systems(path_variable=dict(study_id=820, env_id=cs.context[cs.environment.life_cycle]))
# cs.study_startup(data=cs.context["startup_studies"],
#                  path_variable=dict(study_id=820, env_id=cs.context[cs.environment.life_cycle]))
