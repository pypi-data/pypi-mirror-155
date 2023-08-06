import wx
import wx.xrc


class AlertDialog(wx.Dialog):
    def __init__(self, parent, msg):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"错误提示", pos=wx.DefaultPosition,
                           size=wx.Size(200, 100), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, msg, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)

        bSizer1.Add(self.m_staticText3, 0, wx.ALL, 5)

        self.m_button3 = wx.Button(self, wx.ID_ANY, u"关闭", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_button3, 0, wx.ALL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)
        self.m_button3.Bind(wx.EVT_LEFT_UP, self.close_dialog)

    def __del__(self):
        pass

    def close_dialog(self, event):
        self.Close(True)
        self.GetParent().Enable()


    @classmethod
    def open(cls, parent, msg):
        if parent is not None: parent.Disable()
        error = AlertDialog(parent, msg)
        error.Show()

# if __name__ == '__main__':
#     app = wx.App()
#     main_win = AlertDialog(None, )
#     main_win.Show()
#     app.MainLoop()