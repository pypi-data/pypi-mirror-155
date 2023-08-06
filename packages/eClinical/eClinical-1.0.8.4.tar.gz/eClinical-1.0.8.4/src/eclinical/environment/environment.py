import os

import yaml

from eclinical.execption import required, optional


def value(func):
    def __inner__(self, *args, **kwargs):
        return self.env.get(func.__name__), func.__name__

    return __inner__


class Environment:

    def __init__(self, envir, file_path):
        self.file_path = file_path
        with open(file_path, "r", encoding="utf-8") as f:
            self.env = yaml.load(f.read(), Loader=yaml.FullLoader).get("ENV").get(envir)

    @classmethod
    def loader(cls, envir):
        cur_dir = os.getcwd()
        while os.path.dirname(cur_dir) != cur_dir:
            for root, dirs, files in os.walk(cur_dir):
                for file in files:
                    if file == "environment.yaml":
                        with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                            if yaml.load(f.read(), Loader=yaml.FullLoader).get("ENV").get(
                                envir) is not None: return Environment(envir=envir
                                                                       , file_path=os.path.join(root, file))
            cur_dir = os.path.dirname(cur_dir)
        raise Exception("没有发现配置文件")

    @property
    @required
    @value
    def public_key(self) -> str:
        ...

    @property
    @optional
    @value
    def uri(self) -> str:
        ...

    @property
    @optional
    @value
    def user(self) -> str:
        ...

    @property
    @optional
    @value
    def password(self) -> str:
        ...

    @property
    @optional
    @value
    def company(self) -> str:
        ...

    @property
    @optional
    @value
    def sponsor(self) -> str:
        ...

    @property
    @optional
    @value
    def study(self) -> str:
        ...

    @property
    @optional
    @value
    def life_cycle(self) -> str:
        ...

    @property
    @optional
    @value
    def db(self) -> dict:
        ...


if __name__ == '__main__':
    print(Environment.loader("US_DEMO_EDETEK_PORTAL"))
