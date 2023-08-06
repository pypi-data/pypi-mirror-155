from eclinical.scaffold.inputs.component.text import Text


class Sponsor:
    @classmethod
    def input(cls, msg: str = "请输入申办方名", default=None, default_key=None):
        text = Text(msg, default, default_key)
        return text.get(input(f"{text}\n"))
