import cv2

import mouse
import wx

class Window(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(450, 500))
        self.button=wx.Button(self, -1, 'Запусть', (340, 400), (-1, -1), wx.BU_LEFT, wx.DefaultValidator, "button")
        self.comboBox= wx.ComboBox(self, -1, '', (200, 150), (80, 30), countVebCams(), wx.CB_DROPDOWN, wx.DefaultValidator,"comboBox")
        lable=wx.StaticText(self,-1, 'Выберите камеру', (90,150), (100,30), 0,'lable')
        self.radioBox=wx.RadioBox(self, -1, 'Веберите ведущую руку',(90, 50), (200,75), ["Левая рука", "Правая рука"], 1, 2,
                                  wx.DefaultValidator, "radioBox")
        global indexOpen

        self.Bind(wx.EVT_BUTTON, lambda evt:mouse.mouseContrl(int(self.comboBox.GetSelection()),int(self.radioBox.GetSelection())), self.button)

        self.Show(True)
def OnClick(ind, mainHand):
    mouse.mouseContrl(ind, mainHand)
def countVebCams(): #подсчёт подключенных камер
    index = 0
    arr = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            arr.append(str(index))
        cap.release()
        index += 1
    return arr

app = wx.App()
wnd = Window(None, "Управление мышью")
app.MainLoop()
