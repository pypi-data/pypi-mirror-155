from eclinical.standard.portal.dto.hierarchies.node import Node
from eclinical.standard.portal.dto.hierarchies.study import Study
from eclinical.standard.portal.dto.hierarchy import SponsorExtDto


class Sponsor(Node):
    def __init__(self, sponsorExtDto: SponsorExtDto, parent, relationObjectId):
        super().__init__(sponsorExtDto, parent, relationObjectId)
        # self.relationObjectId = relationObjectId
        self.studyList = [Study(study_dto, self, relationObjectId) for study_dto in sponsorExtDto.studyList()]
        self.level = 1

    # Sponsor 维度选择
    # Sponsor下的study 和 site 全选
    def top_selected(self, relationObjectId):
        self.hasRelation = True
        self.relationObjectId = relationObjectId
        for study in self.studyList:
            study.top_selected()

    def to_dict(self):
        result = super(Sponsor, self).to_dict()
        result["studyList"] = [study.to_dict() for study in self.studyList]
        return result

    @classmethod
    def trees(cls, sponsorExtDtoList: list[SponsorExtDto], relationObjectId):
        return [Sponsor(sponsorExtDto, None, relationObjectId) for sponsorExtDto in sponsorExtDtoList]