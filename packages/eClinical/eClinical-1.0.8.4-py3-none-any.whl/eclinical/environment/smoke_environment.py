import os

from eclinical.environment.environment import Environment


class SmokeEnvironment(Environment):
    def __init__(self, *, envir, path):
        super().__init__(envir, os.path.join(path, "smoke_environment.yaml"))