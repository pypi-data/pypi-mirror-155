from eclinical.scaffold.inputs.component.text import Text


class Port:

    @classmethod
    def input(cls, msg: str = "", default=None, default_key=None):
        text = Text(msg, default, default_key)
        try:
            return int(text.get(input(f"{text}\n")))
        except Exception as e:
            return cls.input("输入非法，请重新输入", default, default_key)
