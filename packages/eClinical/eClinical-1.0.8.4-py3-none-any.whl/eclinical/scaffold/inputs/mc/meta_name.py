from eclinical.scaffold.inputs.component.text import Text


class MetaName:
    @classmethod
    def input(cls, msg: str = "请输入meta名 例如xx_yy", default=None, default_key=None):
        text = Text(msg, default, default_key)
        return text.get(input(f"{text}\n"))