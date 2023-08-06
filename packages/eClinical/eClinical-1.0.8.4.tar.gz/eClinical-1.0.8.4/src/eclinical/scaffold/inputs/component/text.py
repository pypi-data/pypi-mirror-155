class Text:
    def __init__(self, msg: str, default=None, default_key=None):
        self.msg = msg
        self.default = default
        self.default_key = default_key
        self.mapping = {"回车": ""}

    def __repr__(self):
        if self.default:
            return f"{self.msg}, 如使用[{self.default},请按{self.default_key}]"
        return self.msg

    def get(self, value):
        if not self.default:
            if value == "":
                self.msg = "输入不能为空,请再次输入"
                return self.get(input(f"{self}\n"))
            else:
                return value
        elif value == self.mapping.get(self.default_key, self.default_key):
            return self.default
        else:
            return value
