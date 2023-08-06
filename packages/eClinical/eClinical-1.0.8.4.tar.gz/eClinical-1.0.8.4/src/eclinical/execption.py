import warnings


def error(err_msg):
    def __wrapper__(func):
        def __inner__(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            if result[0] is None or len(str(result[0])) == 0: raise Exception(f"{self.file_path} {result[1]} {err_msg}")
            return result[0]
        return __inner__

    return __wrapper__


def warning(warn_msg):
    def __wrapper__(func):
        def __inner__(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            if result[0] is None or len(str(result[0])) == 0:
                warnings.warn(f"{self.file_path} {result[1]} {warn_msg}", Warning, stacklevel=4)
            return result[0]
        return __inner__

    return __wrapper__


def required(func):
    @error(err_msg=f"不能为空")
    def __inner__(self, *args, **kwargs):
        return func(self, *args, **kwargs)
    return __inner__


def optional(func):
    @warning(warn_msg=f"为空")
    def __inner__(self, *args, **kwargs):
        return func(self, *args, **kwargs)
    return __inner__
