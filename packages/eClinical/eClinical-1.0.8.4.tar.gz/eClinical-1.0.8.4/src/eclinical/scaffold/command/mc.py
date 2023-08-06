import argparse
import os

from eclinical.scaffold.files.gen_meta import GemMeta
# from scaffold.files.gen_meta import GemMeta
from eclinical.scaffold.inputs.mc.meta_attrs import MetaAttrs
from eclinical.scaffold.inputs.mc.meta_name import MetaName
from eclinical.scaffold.inputs.mc.meta_type import MetaType

parser = argparse.ArgumentParser()
parser.add_argument("--name", help="创建meta 对象")
parser.add_argument("--type", help="meta 对象类型,mysql 或 json")
parser.add_argument("--attrs", help="对象属性，多个属性以,分割")

args = parser.parse_args()

# TODO 在 meta 中增加帮助示例
class Mc:

    def __init__(self):
        self.folder = os.getcwd()

    def meta(self, meta_name, meta_type, meta_attrs):
        GemMeta(self.folder).add_meta(meta_name, meta_type, meta_attrs)

    def right_path(self):
        if not os.path.exists(os.path.join(self.folder, "meta")):
            raise "没有找到meta文件夹,请确认是在module 文件夹下"


def mc_command():
    try:
        mc = Mc()
        mc.right_path()
        mc.meta(args.name or MetaName().input(),
                args.type or MetaType().input(),
                args.attrs or MetaAttrs().input())
    except Exception as e:
        print(e)


# if __name__ == '__main__':
#     mc_command()
