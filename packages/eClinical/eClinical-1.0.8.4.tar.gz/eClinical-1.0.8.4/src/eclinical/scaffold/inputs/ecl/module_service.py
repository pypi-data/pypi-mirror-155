from eclinical.scaffold.inputs.component.text import Text


class ModuleService:
    @classmethod
    def input(cls, msg="请输入你想创建的service,命名方式'xx_yy'多个Service以','分割", default=None, default_key=None):
        text = Text(msg, default, default_key)
        return text.get(input(f"{text}\n")).split(",")
