from cjen.sco.standard_step import StandardStep

from eclinical.standard.portal.user import User
from eclinical.standard.portal.user_groups import UserGroups
from eclinical.standard.scenarios.portal_scenario import PortalScenario
from eclinical.standard.steps.portal.user.portal_associated_usergroup import PortalAssociatedUserGroup
from eclinical.standard.steps.portal.user.portal_find_user import PortalFindUser
from eclinical.standard.steps.portal.user.portal_find_user_role import PortalFindUserRole
from eclinical.standard.steps.portal.user_groups.portal_find_usergroup import PortalFindUserGroup


class PortalUserAppendUserGroup(StandardStep):
    Name = "portal_user_append_usergroup.py"

    def __init__(self, service: User, scenario: PortalScenario):
        self.service = service
        self.scenario = scenario
        self.service.step_definitions[self.Name] = self

    def _pre_processor(self):
        PortalFindUserGroup(self.service, self.scenario).run()
        PortalAssociatedUserGroup(self.service, self.scenario).run()

    def ignore(self):
        for rels in self.service.context[PortalAssociatedUserGroup.ExistsRels]:
            if self.role_eq(rels) and self.user_group_eq(rels) and self.user_eq(rels):
                return True
        return False

    def role_eq(self, rels):
        return rels.get("roleId") == self.service.context[PortalFindUserRole.Id]

    def user_eq(self, rels):
        return rels.get("userId") == self.service.context[PortalFindUser.Id]

    def user_group_eq(self, rels):
        return rels.get("userGroupId") == self.service.context[PortalFindUserGroup.Id]

    def path_variable(self):
        return dict(user_id=self.service.context[PortalFindUser.Id])

    def data(self):
        rels = self.service.context[PortalAssociatedUserGroup.ExistsRels]
        rels.append(dict(roleId=self.service.context[PortalFindUserRole.Id],
                         userId=self.service.context[PortalFindUser.Id],
                         userGroupId=self.service.context[PortalFindUserGroup.Id]))
        return rels

    def _execute(self):
        self.service.api_append_user_group_role_rel(path_variable=self.path_variable(), data=self.data())
