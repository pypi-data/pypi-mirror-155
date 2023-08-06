from eclinical.scaffold.inputs.component.text import Text


class Study:
    @classmethod
    def input(cls, msg: str = "请输入实验名", default=None, default_key=None):
        text = Text(msg, default, default_key)
        user_input = text.get(input(f"{text}\n"))
        study = "" if user_input == default else user_input
        return study
