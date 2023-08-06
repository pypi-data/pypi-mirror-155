class Meta:

    def __init__(self, name, props=[]):
        self.props = props
        self.name = name

    @property
    def clazz_name(self):
        return "".join([elem.capitalize() for elem in self.name.split("_")])

    def json(self):
        content = "import cjen\nfrom cjen import MetaJson\n\n\n" + f"class {self.clazz_name}(MetaJson):\n"
        content += "    \"\"\"\n    相关使用详情可查询:\n" \
                   "    装饰器: https://github.com/thcpc/cjen#42-metajson-%E8%A3%85%E9%A5%B0%E5%99%A8" \
                   "\n" + \
                   "    \"\"\"\n\n"
        for prop in self.props:
            content += f"    @cjen.operate.common.value\n"
            content += f"    @cjen.operate.json.one(json_path=\"请填写jsonpath\")\n"
            content += f"    def {prop}(self): ...\n\n"
        return content

    def mysql(self):
        content = "import cjen\nfrom cjen import MetaMysql\n\n\n" + f"class {self.clazz_name}(MetaMysql):\n"
        content += "    \"\"\"\n    相关使用详情可查询:\n" \
               "    装饰器: https://github.com/thcpc/cjen#43-metamysql-%E8%A3%85%E9%A5%B0%E5%99%A8\n" +\
               "    \"\"\"\n\n"
        for prop in self.props:
            content += f"    @cjen.operate.common.value\n"
            content += f"    def {prop}(self): ...\n\n"
        return content
