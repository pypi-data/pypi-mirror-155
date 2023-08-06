from eclinical.scaffold.inputs.component.text import Text


class DBHost:
    @classmethod
    def input(cls, msg="请输入数据库主机", default=None, default_key=None):
        text = Text(msg, default, default_key)
        return text.get(input(f"{text}\n"))