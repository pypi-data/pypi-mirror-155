from cjen.sco.scenario import Scenario
from cjen.sco.standard_step import StandardStep

from eclinical.standard.portal.user_groups import UserGroups
from eclinical.standard.scenarios.portal_scenario import PortalScenario
from eclinical.standard.steps.portal.hierarchies.portal_find_sponsor import PortalFindSponsor
from eclinical.standard.steps.portal.user_groups.portal_find_usergroup import PortalFindUserGroup
from eclinical.standard.steps.portal.user_groups.portal_get_company_envs import PortalGetCompanyEnvs
from eclinical.standard.steps.portal.user_groups.portal_get_lifecycle_hierarchies import PortalGetLifeCycleHierarchies


class PortalSetLifeCycleHierarchies(StandardStep):
    Name = "portal_set_lifecycle_hierarchies.py"

    def __init__(self, service: UserGroups, scenario: PortalScenario):
        self.service = service
        self.scenario = scenario
        self.service.step_definitions[self.Name] = self

    def life_cycle(self): return self.scenario.life_cycle()

    def user_group(self): return self.scenario.user_group()

    def _pre_processor(self):
        PortalGetLifeCycleHierarchies(self.service, self.scenario).run()

    def path_variable(self):
        for life_cycle in self.service.context[PortalGetCompanyEnvs.Object]:
            for life_cycle_name, life_cycle_id in life_cycle.items():
                if life_cycle_name == self.life_cycle():
                    return {UserGroups.LifeCycleId: life_cycle_id, UserGroups.UserGroupId: self.service.context[PortalFindUserGroup.Id]}
        return {UserGroups.LifeCycleId: None}

    def sponsor_name(self):
        return self.scenario.sponsor()

    def study_name(self):
        return self.scenario.study()

    def sites_name(self):
        return self.scenario.user_group_sites()

    def data(self):
        for sponsor in self.service.context["hierarchies"]:
            if sponsor.name == self.sponsor_name():
                for study in sponsor.studyList:
                    if study.name == self.study_name():
                        for site in study.siteList:
                            if site.name in self.sites_name():
                                site.selected(self.service.context[PortalFindUserGroup.Id])
                        study.selected(self.service.context[PortalFindUserGroup.Id])
                sponsor.selected(self.service.context[PortalFindUserGroup.Id])
        return [sponsor.to_dict() for sponsor in self.service.context["hierarchies"]]

    def _execute(self):
        self.service.api_set_lifecycle_hierarchies(data=self.data(), path_variable=self.path_variable())
