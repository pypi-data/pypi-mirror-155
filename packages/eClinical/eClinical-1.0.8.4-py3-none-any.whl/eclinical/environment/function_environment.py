import os

from eclinical.environment.environment import Environment


class FunctionEnvironment(Environment):
    def __init__(self, *, envir, path):
        super().__init__(envir, os.path.join(path, "function_environment.yaml"))