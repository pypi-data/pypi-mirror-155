class Radio:
    def __init__(self, msg: str, select: tuple):
        self.select = select
        self.msg = msg

    def __repr__(self):
        string = f"{self.msg}["
        string += ",".join([f"{i+1}:{v}" for i, v in enumerate(self.select)])
        string += "]"
        return string

    def get(self, index):
        if index < 1 or index > len(self.select):
            raise Exception(f"{index} 非法输入")
        return self.select[index-1]
