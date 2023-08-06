from eclinical.standard.portal.dto.hierarchies.node import Node
from eclinical.standard.portal.dto.hierarchy import SiteDto


class Site(Node):
    def __init__(self, value: SiteDto, parent:Node, relationObjectId):
        super().__init__(value, parent, relationObjectId)
        self.level = 3
        self.sponsorId = parent.parentId
        self.studyId = parent.id
        self.name = value.code()

    # 从Site 维度选择，对应的Study和Sponsor都应该选中
    def selected(self, relationObjectId):
        super(Site, self).selected(relationObjectId)
        self.parent.selected(relationObjectId)
    
    def to_dict(self):
        result = super(Site, self).to_dict()
        result["sponsorId"] = self.sponsorId
        result["studyId"] = self.studyId
        return result

    def __top_selected(self): self.hasRelation = True


