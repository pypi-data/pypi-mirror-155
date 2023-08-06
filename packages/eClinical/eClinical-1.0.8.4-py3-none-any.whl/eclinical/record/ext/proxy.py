import winreg
import ctypes


class Proxy:

    def __init__(self):
        self.internet_settings = None
        self.init_internet_settings()

    def set_key(self, name, value, reg_type):
        winreg.SetValueEx(self.internet_settings, name, 0, reg_type, value)

    def init_internet_settings(self):
        try:
            self.internet_settings = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                                    r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
                                                    0, winreg.KEY_ALL_ACCESS)
        except OSError as e:
            print(e)

    def open(self):
        # 启用代理
        self.set_key('ProxyEnable', 1, winreg.REG_DWORD)  # 启用
        self.set_key('ProxyOverride', u'*.local;<local>', winreg.REG_SZ)  # 绕过本地
        self.set_key('ProxyServer', u'127.0.0.1:9999', winreg.REG_SZ)  # 代理IP及端口，将此代理修改为自己的代理IP

    def close(self):
        self.set_key('ProxyEnable', 0, winreg.REG_DWORD)  # 停用


win_proxy = Proxy()
