import wx
from Printer import Printer
from InputHandler import InputHandler
from Constants import FPS


class GameFrame(wx.Frame):
    def __init__(self, game):
        super(GameFrame, self).__init__(None, title='Zoo', size=(800, 800))
        self.printer = Printer(self)

        self.game = game
        self.notifications = []
        self.game.printer = self.printer
        self.game.set_notifications(self.notifications)
        self.notificationsWindow = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP)

        self.inputHandler = InputHandler(self)

        # arrange stuff
        box = wx.BoxSizer(orient=wx.VERTICAL)
        box.Add(self.printer, 15, flag=wx.ALL, border=5)
        box.Add(self.notificationsWindow, 3, flag=wx.ALL | wx.EXPAND, border=5)
        box.Add(self.inputHandler, -1, flag=wx.ALL | wx.EXPAND, border=5)

        self.update_loop()

        self.SetSizer(box)
        self.Center()
        self.Show()

    def update_loop(self):
        self.game.update()
        while self.notifications:
            self.notify(self.notifications.pop(0))
        wx.CallLater(1000//FPS, self.update_loop)

    def notify(self, message):
        self.notificationsWindow.AppendText(message + '\n')
