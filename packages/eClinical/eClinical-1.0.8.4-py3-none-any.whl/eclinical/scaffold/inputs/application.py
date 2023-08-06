from eclinical.scaffold.inputs.component.radio import Radio


class Application:
    @classmethod
    def input(cls, msg, select=("portaladmin", "portal", "ctms", "etmf", "design", "edc", "iwrs", "eConsent(暂时不支持)", "pv",
                     "IDP(暂不支持)", "非Application")):
        radio = Radio(msg, select)
        try:
            return radio.get(int(input(f"{radio}\n")))
        except Exception as e:
            return cls.input(f"输入非法，请重新输入{msg}")
