from eclinical.scaffold.inputs.component.text import Text


class Schema:
    @classmethod
    def input(cls, msg: str = "请输入访问数据库的schema", default=None, default_key=None):
        text = Text(msg, default, default_key)
        return text.get(input(f"{text}\n"))
