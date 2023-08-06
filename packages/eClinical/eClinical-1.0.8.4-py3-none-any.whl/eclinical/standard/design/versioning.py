import cjen

from eclinical import DesignLoginService, Environment
from eclinical.standard.design.dto.archive_file import ArchiveFiles
from eclinical.standard.design.dto.version_info import VersionInfo


class Versioning(DesignLoginService):
    def __init__(self, environment: Environment):
        super().__init__(environment)

    @cjen.http.get_mapping(uri="design/crf/version/list", json_clazz=VersionInfo)
    @cjen.operate.asserts.validation_meta(meta_name="version_info", fields="procCode")
    def version_list(self, version_info: VersionInfo = None, resp=None, **kwargs):
        from eclinical.standard.steps.design.versioning.design_get_last_version import DesignGetLastVersion
        self.step_definitions.call_back(DesignGetLastVersion.Name, version_info=version_info)

    @cjen.http.post_mapping(uri="design/crf/version/download")
    def download_file(self, data, resp=None, **kwargs):
        from eclinical.standard.steps.design.versioning.design_download_publish_sql import DesignDownloadPublishSql
        self.step_definitions.call_back(DesignDownloadPublishSql.Name, file_bytes=resp)

    @cjen.http.get_mapping(uri="design/crf/version/archive-file?currentVersionId={currentVersionId}",
                           json_clazz=ArchiveFiles)
    @cjen.operate.asserts.validation_meta(meta_name="archives", fields="procCode")
    def archive_files(self, path_variable, archives: ArchiveFiles = None, resp=None, **kwargs):
        from eclinical.standard.steps.design.versioning.design_fileids import DesignFileIDS
        self.step_definitions.call_back(DesignFileIDS.Name, archives=archives)
