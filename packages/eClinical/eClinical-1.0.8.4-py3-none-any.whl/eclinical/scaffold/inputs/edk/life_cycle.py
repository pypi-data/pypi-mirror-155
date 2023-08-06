from eclinical.scaffold.inputs.component.radio import Radio


class LifeCycle:
    @classmethod
    def input(cls, msg: str = "请输入项目阶段", select=("dev", "uat", "prod")):
        radio = Radio(msg, select)
        try:
            return radio.get(int(input(f"{radio}\n")))
        except Exception as e:
            return cls.input("输入非法，请重新输入项目阶段")