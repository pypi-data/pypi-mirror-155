import os.path
from typing import IO

# import cjen.dada.smile
import cjen
from cjen.dada import smile
import mitmproxy
from urllib.parse import urlparse, parse_qs, urlunsplit, urlunparse, parse_qsl

from eclinical.record.ext.api.api_spec import ApiSpec
from eclinical.record.ext.api.swagger import Swagger
from eclinical.scaffold.template.service import Service


# TODO 装饰器添加方法
# TODO 装饰器如果不存在文件，则生成文件，已存在则忽略


# @cjen.dada.smile.haha()
# def new_file():


def create_service(func):
    def __inner__(self):
        if not os.path.exists(f'{self.service_template.file_name}.py'):
            @cjen.haha(LogPath=os.path.curdir, LogName=f'{self.service_template.file_name}.py', Mode='a')
            def write(msg, io: IO):  io.write(msg)
            write(self.service_template.output_service_py())
        func(self)
        return __inner__

    return __inner__


class EclinicalService:
    def __init__(self, flow):
        self.flow = flow
        self.service_template = Service(service_name=self.name, app=self.app)

    @property
    def name(self):
        return self.flow.request.path.split("/")[2]

    @property
    def app(self):
        if self.name == "admin":
            return "portal"
        return self.name

    @property
    def method(self): return self.flow.request.method

    @property
    def api_url(self):
        # api = "/".join(self.flow.request.path.split("/")[2:])
        return ApiSpec.api(Swagger(), self.flow.request)
        # result = urlparse(api)
        # query = "&".join([f'{key}={{{key}}}' for key in parse_qs(result.query).keys()])
        # return urlunparse(["", "", result.path, result.params, query, result.fragment])

    def generate(self):
        self.append_api()

    @create_service
    def append_api(self):
        @cjen.haha(LogPath=os.path.curdir, LogName=f'{self.service_template.file_name}.py', Mode='a')
        def write(msg, io: IO):  io.write(msg)
        self.service_template.output_method(self.api_url, self.flow)
        # write(self.api_url + "\n")

