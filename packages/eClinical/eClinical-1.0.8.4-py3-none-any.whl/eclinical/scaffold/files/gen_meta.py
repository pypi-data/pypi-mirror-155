import os

from eclinical.scaffold.inputs.mc.meta_service import MetaService
from eclinical.scaffold.template.file_operate import FileOperate
from eclinical.scaffold.template.meta import Meta
# from scaffold.template.meta import Meta


class GemMeta:
    def __init__(self, folder):
        self.folder = folder

    def add_meta(self, meta_name: str, meta_type: str, props: list[str]):
        meta = Meta(meta_name, props)
        fop = FileOperate(self.folder)

        service = self.belong_service()

        body = meta.json() if meta_type == 'Json' else meta.mysql()

        sub_folder = os.path.join("meta", service) if service is not None else "meta"
        if not os.path.exists(os.path.join(self.folder, sub_folder)):
            os.mkdir(os.path.join(self.folder, sub_folder))
        fop.rewrite_file(sub_folder, meta.name + ".py", body) \
        or fop.new_file(sub_folder, meta.name + ".py", body)

    @classmethod
    def ok_response(cls, folder: str):
        body = """
import cjen
from cjen import MetaJson


class OKResponse(MetaJson):
    @cjen.operate.asserts.equal(value=200)
    @cjen.operate.json.one(json_path="$.procCode")
    def procCode(self): ...
"""
        fop = FileOperate(folder)
        fop.rewrite_file("meta", "ok_response.py", body) \
        or fop.new_file("meta", "ok_response.py", body)

    def belong_service(self):
        services = ["不属于任何service"]
        for root, folder, files in os.walk(os.path.join(self.folder, "services")):
            for file in files:
                if file.endswith("_service.py"):
                    services.append(file.replace(".py", ""))
        service = MetaService.input(select=tuple(services))
        if service == "不属于任何service": return None
        return service
