# from scaffold.command.edk import Edk
from eclinical.scaffold.inputs.component.text import Text


class EnvironmentName:
    @classmethod
    def input(cls, edk, msg: str = "请输入 environment 名", default=None, default_key=None):
        text = Text(msg, default, default_key)
        name = text.get(input(f"{text}\n"))
        if edk.environment_exist(name):
            return cls.input(edk, "environment 名已存在,请重新输入", default, default_key)
        else:
            return name
