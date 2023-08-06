import argparse
import os

from eclinical.scaffold.files.gen_service import GenService
from eclinical.scaffold.inputs.application import Application
from eclinical.scaffold.inputs.ecl.module_name import ModuleName
from eclinical.scaffold.inputs.ecl.module_service import ModuleService
from eclinical.scaffold.inputs.ecl.module_type import ModuleType
from eclinical.scaffold.template.file_operate import FileOperate
from eclinical.scaffold.files.gen_meta import GemMeta
from eclinical.scaffold.template.service import Service

parser = argparse.ArgumentParser()
parser.add_argument("-init", action='store_true', help="初始化一个module，包括生成environment.yaml，全局的conftest")
parser.add_argument("-ns", action='store_true', help="执行初始化module时，如果带这个参数，表明创建Module 同时创建 service")
args = parser.parse_args()


class Ecl:

    def __init__(self, name=None, module_type=None):
        self.name = name
        self.module_type = module_type
        self.ecl_folder = os.path.join(os.getcwd(), f'{self.name}_{self.module_type}')

    def init_module(self):
        if os.path.exists(self.ecl_folder): raise Exception("请勿重复创建")
        os.mkdir(self.ecl_folder)
        os.mkdir(os.path.join(self.ecl_folder, "services"))
        os.mkdir(os.path.join(self.ecl_folder, "meta"))
        os.mkdir(os.path.join(self.ecl_folder, "ext"))
        FileOperate(self.ecl_folder).new_file("", "__init__.py", "")
        if self.module_type == "testcase":
            FileOperate(self.ecl_folder).new_file("", "conftest.py", Service.output_conftest_header_py())
            GemMeta.ok_response(self.ecl_folder)


def ecl_command():
    if args.init:
        ecl = Ecl(ModuleName.input(), ModuleType.input())
        ecl.init_module()
        if args.ns:
            for service_name in ModuleService.input():
                gen = GenService(ecl.ecl_folder)
                gen.add_service(service_name, Application.input(msg=f"{service_name}是什么系统"))
                # ecl.add_service(service_name, Application.input(msg=f"{service_name}是什么系统"))

# if __name__ == '__main__':
#     ecl_command()
