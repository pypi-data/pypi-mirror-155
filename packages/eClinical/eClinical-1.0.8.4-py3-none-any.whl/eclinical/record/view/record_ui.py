# -*- coding: utf-8 -*-
from urllib.parse import urlparse

import wx
import wx.xrc
from mitmproxy.tools.main import mitmweb

# from record.parameter import Parameter
# from record.record_service import RecordService
from eclinical.record.ext.common import disable_elements, enable_elements, empty_string
from eclinical.record.ext.memcached import memcached
from eclinical.record.ext.proxy import Proxy, win_proxy
from eclinical.record.mitm.mitm_process import MitmProcess
from eclinical.record.view.alert_dialog import AlertDialog
from eclinical.record.view.status import Status


# from test import mock_upload, mock_upload_error, mock_record_error

# TODO 保存在工程目录中
# TODO 配置读取Enviroment文件
class RecordUi(wx.Frame):

    def __init__(self, parent, envirs):
        self.status_list = [Status.INIT]
        self.proxy = Proxy()
        self.record_service = None
        self.envirs = envirs
        # height = len(envirs) * 35
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="接口录制", pos=wx.DefaultPosition,
                          size=wx.Size(self.width(), self.height()), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.Size(self.width(), self.height()), wx.Size(self.width(), self.height()))
        self.mitm_process = None
        fgSizer1 = wx.FlexGridSizer(4, 2, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, u"服务器列表", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)

        fgSizer1.Add(self.m_staticText3, 0, wx.ALL, 5)

        # fgSizer1.Add(self.m_staticText41, 0, wx.ALL, 5)

        m_listBox2Choices = [name for name in envirs.keys()]
        self.m_listBox2 = wx.ListBox(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_listBox2Choices, 0)

        fgSizer1.Add(self.m_listBox2, 0, wx.ALL, 5)

        self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"Json存放路径", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)

        fgSizer1.Add(self.m_staticText4, 0, wx.ALL, 5)

        self.test_name = wx.TextCtrl(self, wx.ID_ANY, "ecd", wx.DefaultPosition, wx.DefaultSize, 0)
        self.test_name.Disable()
        fgSizer1.Add(self.test_name, 0, wx.ALL, 5)

        self.start_button = wx.Button(self, wx.ID_ANY, u"启动", wx.DefaultPosition, wx.DefaultSize, 0)
        self.start_button.Enable()
        fgSizer1.Add(self.start_button, 0, wx.ALL, 5)

        self.stop_button = wx.Button(self, wx.ID_ANY, u"停止", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stop_button.Disable()
        fgSizer1.Add(self.stop_button, 0, wx.ALL, 5)

        # self.upload_button = wx.Button(self, wx.ID_ANY, u"上传", wx.DefaultPosition, wx.DefaultSize, 0)
        # self.upload_button.Disable()
        #
        # fgSizer1.Add(self.upload_button, 0, wx.ALL, 5)
        # self.m_dirPicker1 = wx.DirPickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"请选择文件夹", wx.DefaultPosition,
        #                                      wx.DefaultSize,
        #                                      wx.DIRP_DEFAULT_STYLE)
        # fgSizer1.Add(self.m_dirPicker1, 0, wx.ALL, 5)
        #
        self.SetSizer(fgSizer1)
        self.Layout()

        self.Centre(wx.BOTH)
        # Connect Events
        self.start_button.Bind(wx.EVT_LEFT_UP, self.evt_start_up)
        self.stop_button.Bind(wx.EVT_LEFT_UP, self.evt_shut_down)
        # self.m_dirPicker1.Bind(wx.EVT_DIRPICKER_CHANGED, self.evt_select_folder)

    def __del__(self):
        pass

    def height(self):
        if len(self.envirs) * 25 + 200 > 326: return 326
        return len(self.envirs) * 10 + 200

    def width(self):
        max_item = 0

        def chinese(ch):
            return '\u4e00' <= ch <= '\u9fff'

        for value in self.envirs.keys():
            item = 0
            for ch in value:
                if chinese(ch):
                    item += 18
                else:
                    item += 8
            if item > max_item:
                max_item = item
        if max_item + 112 > 256: return max_item + 112 + 30
        return 256

    def change_status(self, new_status, msg=None):
        self.__append(new_status)
        self.status_evt(self.__peek(), msg)
        self.__pops(Status.UPLOADING_FINISH, Status.PREPARE_UPLOADING)
        self.__pops(Status.RECORDING_FINISH, Status.PREPARE_RECORDING)
        print(self.status_list)

    def __suspend(self):
        while True:
            status = self.__peek()
            if status == Status.PREPARE_RECORDING: break
            if status == Status.PREPARE_UPLOADING: break
            self.__pop()

    def __pops(self, begin, end):
        if self.__peek() == begin:
            while True:
                status = self.__pop()
                if status == end: break

    def __append(self, status):
        if self.__peek() == status:
            pass
        elif status == Status.PREPARE_RECORDING or status == Status.PREPARE_UPLOADING:
            if self.status_list[len(self.status_list) - 1] == Status.INIT:
                self.status_list.append(status)
            else:
                self.status_list[len(self.status_list) - 1] = status
        else:
            self.status_list.append(status)

    def __pop(self):
        return self.status_list.pop()

    def __peek(self):
        return self.status_list[len(self.status_list) - 1]

    def evt_start_up(self, event):
        self.change_status(Status.PREPARE_RECORDING)
        self.change_status(Status.RECORDING)
        if self.validation_record():
            memcached.set("host", self.parameter_host())
            memcached.set("folder", self.parameter_test_name())
            self.service_record_start()

    def evt_shut_down(self, event):
        self.change_status(Status.RECORDING_FINISH)
        self.service_record_stop()

    # def evt_select_folder(self, event):
    #     self.change_status(Status.PREPARE_UPLOADING)
    #
    # def validation_upload(self):
    #     if empty_string(self.m_dirPicker1.GetPath()):
    #         self.change_status(Status.ERROR, u"测试的数据文件不正确")
    #         return False
    #     return True

    def validation_record(self):
        if self.m_listBox2.GetSelection() == -1:
            self.change_status(Status.ERROR, u"请选择服务器列表")
            return False

        if empty_string(self.test_name.GetValue()):
            self.change_status(Status.ERROR, u"请简诉录制内容")
            return False
        return True

    def ui_disable_running(self):
        disable_elements(self.start_button,
                         self.test_name, self.m_listBox2, self.stop_button)

    def ui_enable_all(self):
        enable_elements(self.start_button,
                        self.test_name, self.m_listBox2, self.stop_button)

    def status_evt(self, status, msg=None):

        if status == Status.RECORDING:
            self.ui_disable_running()
            enable_elements(self.stop_button)
        elif status == Status.PREPARE_RECORDING:
            self.ui_enable_all()
            # disable_elements(self.upload_button)
            disable_elements(self.stop_button)
        elif status == Status.ERROR:
            AlertDialog.open(self, msg)
            self.__suspend()
            self.change_status(self.__peek())
        elif status == Status.RECORDING_FINISH:
            self.ui_enable_all()
            disable_elements(self.stop_button)
        elif status == Status.PREPARE_UPLOADING:
            self.ui_enable_all()
        elif status == Status.UPLOADING:
            self.ui_disable_running()
        elif status == Status.UPLOADING_FINISH:
            self.ui_enable_all()
            disable_elements(self.stop_button)

    def parameter_host(self):
        return self.envirs.get(self.m_listBox2.GetStringSelection())

    def parameter_test_name(self):
        return self.test_name.GetValue()

    def service_record_start(self):
        win_proxy.open()
        self.get_mitm_process().set_host(urlparse(self.parameter_host()).hostname)

        self.get_mitm_process().start()
        # mitm_process.start()

    def get_mitm_process(self):
        if self.mitm_process is None:
            self.mitm_process = MitmProcess()
        return self.mitm_process

    def service_record_stop(self):
        win_proxy.close()
        self.get_mitm_process().stop()
        self.mitm_process = None
