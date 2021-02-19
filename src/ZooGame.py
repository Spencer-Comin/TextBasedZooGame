from GameWindow import GameFrame
from Game import Game
import wx


if __name__ == '__main__':
    app = wx.App()
    frame = GameFrame(Game('zoo.txt'))
    app.MainLoop()
