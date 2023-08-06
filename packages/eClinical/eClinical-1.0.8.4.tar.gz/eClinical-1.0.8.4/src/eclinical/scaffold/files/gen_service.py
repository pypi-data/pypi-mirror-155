import os

from eclinical.scaffold.template.file_operate import FileOperate
from eclinical.scaffold.template.service import Service
# from scaffold.template.service import Service


class GenService:
    def __init__(self, folder):
        self.folder = folder

    def add_service(self, service_names: str, app: str):
        for service_name in service_names.split(","):
            service = Service(service_name, app)
            # 输出到service.py
            if not os.path.exists(os.path.join(self.folder, "services")): os.mkdir(
                os.path.join(self.folder, "services"))
            fop = FileOperate(self.folder)
            if fop.file_exist("services", service.file_name):
                if input(f"{service.service_name} 已存在，是否覆盖(Y/N)") == 'N':
                    continue
            fop.rewrite_file("services", service.file_name + ".py", service.output_service_py()) \
            or fop.new_file("services", service.file_name + ".py", service.output_service_py())
            # 输出到 __init__.py
            fop.append_file("services", "__init__.py", service.output_init_py()) \
            or fop.new_file("services", "__init__.py", service.output_init_py())
            # 输出到 conftest.py
            fop.append_file("", "conftest.py", service.output_conftest_body_py()) \
            or fop.new_file("", "conftest.py", service.output_conftest_body_py())

