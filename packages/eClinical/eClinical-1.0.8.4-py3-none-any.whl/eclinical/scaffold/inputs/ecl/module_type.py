from eclinical.scaffold.inputs.component.radio import Radio


class ModuleType:

    @classmethod
    def input(cls, msg: str = "请输入Module类型", select=("testcase", "helper")):
        radio = Radio(msg, select)
        try:
            return radio.get(int(input(f"{radio}\n")))
        except Exception as e:
            return cls.input("输入非法，请重新输入Module类型")
