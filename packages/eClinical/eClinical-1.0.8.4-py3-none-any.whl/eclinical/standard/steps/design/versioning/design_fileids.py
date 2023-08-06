from cjen.sco.scenario import Scenario
from cjen.sco.standard_step import StandardStep

from eclinical.standard.design.versioning import Versioning
from eclinical.standard.steps.design.versioning.design_get_last_version import DesignGetLastVersion


# 获取生成文件的fileid
class DesignFileIDS(StandardStep):
    Name = "design_fileids.py"

    def __init__(self, service: Versioning, scenario: Scenario):
        self.service = service
        self.scenario = scenario
        self.service.step_definitions[self.Name] = self

    def _pre_processor(self):
        DesignGetLastVersion(self.service, self.scenario).run()

    def _execute(self):  self.service.archive_files(path_variable=self.path_variable())

    def call_back(self, **kwargs):
        self.service.context["archives"] = kwargs.get("archives")

    def path_variable(self):
        return dict(currentVersionId=self.service.context["currentVersionId"])
