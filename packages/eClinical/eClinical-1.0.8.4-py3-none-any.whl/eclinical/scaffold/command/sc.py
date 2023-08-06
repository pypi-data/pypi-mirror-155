import argparse
import os

from eclinical.scaffold.files.gen_service import GenService
from eclinical.scaffold.inputs.application import Application

# from scaffold.files.gen_service import GenService
from eclinical.scaffold.inputs.sc.service_name import ServiceName

parser = argparse.ArgumentParser()
parser.add_argument("-name", help="创建或更新的 service 名")
args = parser.parse_args()


class Sc:
    def __init__(self, name):
        self.name = name
        self.folder = os.getcwd()

    def path_right(self):
        if not os.path.exists(os.path.join(self.folder, "services")):
            raise Exception("无法找到services文件夹")


def sc_command():
    try:
        name = args.name or ServiceName.input()
        sc = Sc(name)
        sc.path_right()
        GenService(sc.folder).add_service(name, Application.input(msg=f"{name}是什么系统"))
    except Exception as e:
        print(e)

# if __name__ == '__main__':
#     sc_command()
