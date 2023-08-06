import os


class FileOperate:
    def __init__(self, folder):
        self.folder = folder

    def rewrite_file(self, sub_folder, file_name, content):
        if self.file_exist(sub_folder, file_name):
            re_write = input(f"{file_name} 已存在,是否覆盖(Y/N)")
            if re_write.lower() == 'y':
                with open(os.path.join(self.folder, sub_folder, file_name), 'w', encoding="utf-8") as f:
                    f.write(content)
            return True
        return False

    def new_file(self, sub_folder, file_name, content):
        with open(os.path.join(self.folder, sub_folder, file_name), 'w', encoding="utf-8") as f:
            f.write(content)
        return True

    def append_file(self, sub_folder, file_name, content):
        if self.file_exist(sub_folder, file_name):
            with open(os.path.join(self.folder, sub_folder, file_name), 'a', encoding="utf-8") as f:
                f.write(content)
            return True
        return False

    def file_exist(self, sub_folder, file_name):
        return os.path.exists(os.path.join(self.folder, sub_folder, file_name))
