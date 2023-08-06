
from eclinical.standard.portal.dto.hierarchy import SponsorExtDto


class Node:
    def __init__(self, value, parent, relationObjectId):
        self.parent = parent
        self.hasRelation = value.hasRelation()
        self.relationObjectId = relationObjectId if self.hasRelation else None
        self.id = value.id()
        self.level = None
        self.name = value.name()
        self.parentId = parent.id if parent is not None else None

    def selected(self, relationObjectId):
        self.hasRelation = True
        self.relationObjectId = relationObjectId


    def to_dict(self):
        return dict(hasRelation=self.hasRelation,
                    id=self.id, level=self.level, name=self.name, parentId=self.parentId,
                    relationObjectId=self.relationObjectId)


