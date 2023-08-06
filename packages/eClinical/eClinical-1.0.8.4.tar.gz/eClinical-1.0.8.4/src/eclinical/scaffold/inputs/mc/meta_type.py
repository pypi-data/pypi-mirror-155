from eclinical.scaffold.inputs.component.radio import Radio


class MetaType:
    @classmethod
    def input(cls, msg: str = "请输入meta的类型", select=("Mysql", "Json")):
        radio = Radio(msg, select)
        try:
            return radio.get(int(input(f"{radio}\n")))
        except Exception as e:
            return cls.input("输入非法，meta的类型")