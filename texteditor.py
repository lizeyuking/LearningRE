# import wx
# class ExampleFrame(wx.Frame):
#     def __init__(self, parent):
#         wx.Frame.__init__(self, parent)
#
#         self.panel = wx.Panel(self)
#         self.quote = wx.StaticText(self.panel, label="Your quote:")
#         self.result = wx.StaticText(self.panel, label="")
#         self.result.SetForegroundColour(wx.RED)
#         self.button = wx.Button(self.panel, label="Save")
#         self.lblname = wx.StaticText(self.panel, label="Your name:")
#         self.editname = wx.TextCtrl(self.panel, size=(140, -1))
#
#         # Set sizer for the frame, so we can change frame size to match widgets
#         self.windowSizer = wx.BoxSizer()
#         self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)
#
#         # Set sizer for the panel content
#         self.sizer = wx.GridBagSizer(5, 5)
#         self.sizer.Add(self.quote, (0, 0))
#         self.sizer.Add(self.result, (0, 1))
#         self.sizer.Add(self.lblname, (1, 0))
#         self.sizer.Add(self.editname, (1, 1))
#         self.sizer.Add(self.button, (2, 0), (1, 2), flag=wx.EXPAND)
#
#         # Set simple sizer for a nice border
#         self.border = wx.BoxSizer()
#         self.border.Add(self.sizer, 1, wx.ALL | wx.EXPAND, 5)
#
#         # Use the sizers
#         self.panel.SetSizerAndFit(self.border)
#         self.SetSizerAndFit(self.windowSizer)
#
#         # Set event handlers
#         self.button.Bind(wx.EVT_BUTTON, self.OnButton)
#
#     def OnButton(self, e):
#         i = 0
#         a = 'a'
#         while (i <= 10000000000):
#             self.result.SetLabel(a)
#             i += 1
#             a = a + 'a'
#
# app = wx.App(False)
# frame = ExampleFrame(None)
# frame.Show()
# app.MainLoop()
#文本编辑器
import wx
app = wx.App()
win = wx.Frame(None, title="自动RE生成器", size=(600, 400))
negpath = ''
pospath = ''
bkg = wx.Panel(win)     #背景板id
i = 0
BestRe = "123456789101112131415"
BestF1 = 0
def openFile(evt):          #打开指定数据集文件
    dlg = wx.FileDialog(
        win,
        "Open",
        "",
        "",
        "All files (*.*)|*.*",
        wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
    filepath = ''
    if dlg.ShowModal() == wx.ID_OK:
        filepath = dlg.GetPath()            #找到文件地址
    else:
        return
    #将文件内容写在
    filename.SetValue(filepath)         #将文件地址写进文本框里
    global pospath
    pospath = filepath
    fopen = open(filepath)
    fcontent = fopen.read()
    contents.SetValue(fcontent)
    fopen.close()

def openFile1(evt):          #打开指定反例文件
    dlg = wx.FileDialog(
        win,
        "Open",
        "",
        "",
        "All files (*.*)|*.*",
        wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
    filepath1 = ''
    if dlg.ShowModal() == wx.ID_OK:
        filepath1 = dlg.GetPath()            #找到文件地址
    else:
        return
    #将文件内容写在
    filename1.SetValue(filepath1)         #将文件地址写进文本框里
    global negpath
    negpath = filepath1
    fopen = open(filepath1)
    fcontent = fopen.read()
    contents.SetValue(fcontent)
    fopen.close()

def saveFile(evt):

    fcontent = contents.GetValue()
    fopen = open(filename.GetValue(), 'w')
    fopen.write(fcontent)
    fopen.close()
    win = wx.Frame(None, title='正反例集')
    button = wx.Button(win, label='保存成功')
    win.Show()
    #contents.SetValue("")
def Runall(evt):
    i = 0
    while (i <10000):
        global BestRe
        global BestF1
        global BestF1
        BestF1 += 1

        ReTxt.SetLabel(BestRe)
        F1Txt.SetLabel(str(BestF1))
        #BestRe = BestRe+'a'
        i = i + 1

openBtn1 = wx.Button(bkg, label='正例集')
openBtn1.Bind(wx.EVT_BUTTON, openFile)   #事件绑定
openBtn2 = wx.Button(bkg, label='反例集')
openBtn2.Bind(wx.EVT_BUTTON, openFile1)   #事件绑定
rungame = wx.Button(bkg, label = 'RE')
rungame.Bind(wx.EVT_BUTTON, Runall)   #事件绑定

saveBtn = wx.Button(bkg, label='确定')
saveBtn.Bind(wx.EVT_BUTTON, saveFile)
saveBtn1 = wx.Button(bkg, label='确定')
saveBtn1.Bind(wx.EVT_BUTTON, saveFile)

filename = wx.TextCtrl(bkg, style=wx.TE_READONLY)   #不可编辑文本控件
filename1 = wx.TextCtrl(bkg, style=wx.TE_READONLY)   #不可编辑文本控件
contents = wx.TextCtrl(bkg, style=wx.TE_MULTILINE)  #文本控件允许多行编辑
ReValue = wx.TextCtrl(bkg, style=wx.TE_READONLY)
ReValue.SetValue('目前最好RE=> ')
F1Value = wx.TextCtrl(bkg, style=wx.TE_READONLY)
F1Value.SetValue( 'f1测度=>' )
ReTxt = wx.StaticText(bkg,label = '          ' ,style = wx.ALIGN_CENTER)
F1Txt = wx.StaticText(bkg,label = '          ' ,style = wx.ALIGN_CENTER)

hbox = wx.BoxSizer(wx.HORIZONTAL)       #水平布局
hbox.Add(openBtn1, proportion=0, flag=wx.LEFT | wx.ALL, border=5)
hbox.Add(filename, proportion=1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=5)
hbox.Add(saveBtn, proportion=0, flag=wx.LEFT | wx.ALL, border=5)

hbox1 = wx.BoxSizer(wx.HORIZONTAL)
hbox1.Add(openBtn2, proportion=0, flag=wx.LEFT | wx.ALL, border=5)
hbox1.Add(filename1, proportion=1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=5)
hbox1.Add(saveBtn1, proportion=0, flag=wx.LEFT | wx.ALL, border=5)

hbox2 = wx.BoxSizer(wx.HORIZONTAL)
hbox2.Add(rungame, proportion=2, flag=wx.LEFT | wx.ALL, border=5)
hbox2.Add(ReValue,1,wx.ALIGN_LEFT)
hbox2.Add(ReTxt, proportion=3, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=5)
hbox2.Add(F1Value,1,wx.ALIGN_LEFT)
hbox2.Add(F1Txt, proportion=1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=5)


bbox = wx.BoxSizer(wx.VERTICAL)
bbox.Add(hbox, proportion=0, flag=wx.EXPAND | wx.ALL)
bbox.Add(hbox1, proportion=0, flag=wx.EXPAND | wx.ALL)
bbox.Add(contents, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)
bbox.Add(hbox2, proportion=0, flag=wx.EXPAND | wx.ALL)


bkg.SetSizer(bbox)
win.Show()
app.MainLoop()


#
#
#
#
