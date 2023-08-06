from eclinical.scaffold.inputs.component.text import Text


class MetaAttrs:
    @classmethod
    def input(cls, msg="请输入对象属性，多个属性以','分割", default=None, default_key=None):
        text = Text(msg, default, default_key)
        attrs = text.get(input(f"{text}\n")).split(",")
        if len(attrs) != len(set(attrs)):
            return cls.input("输入非法，meta的类型属性不能有相同的名字")
        return attrs


if __name__== '__main__':
    a  = [1,2,1]
    b = set(a)
    print(len(a),len(b))