from eclinical.scaffold.inputs.component.radio import Radio


class MetaService:
    @classmethod
    def input(cls, msg: str = "请输入该meta对象属于的service", select=("", "")):
        radio = Radio(msg, select)
        try:
            return radio.get(int(input(f"{radio}\n")))
        except Exception as e:
            return cls.input("输入非法，请输入该meta对象属于的service")