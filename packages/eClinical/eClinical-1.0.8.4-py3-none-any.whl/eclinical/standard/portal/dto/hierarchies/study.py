from eclinical.standard.portal.dto.hierarchies.node import Node
from eclinical.standard.portal.dto.hierarchies.site import Site
from eclinical.standard.portal.dto.hierarchy import StudyDto


class Study(Node):
    def __init__(self, value: StudyDto, parent: Node, relationObjectId):
        super().__init__(value, parent, relationObjectId)
        self.level = 2
        self.sponsorId = None
        self.siteList = [Site(site_dto, self, relationObjectId) for site_dto in value.siteList()]

    def selected(self, relationObjectId):
        super(Study, self).selected(relationObjectId)
        self.parent.selected(relationObjectId)

    # Study 维度选择
    def top_selected(self):
        self.hasRelation = True
        # 选中上级Sponsor
        self.parent.selected()
        # 选中该study下的所有Site
        for site in self.siteList:
            site.__top_selected()

    def to_dict(self):
        result = super(Study, self).to_dict()
        result["siteList"] = [study.to_dict() for study in self.siteList]
        return result
