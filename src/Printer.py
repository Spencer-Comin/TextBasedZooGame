import wx


class Printer(wx.StaticText):
    def __init__(self, parent):
        super(Printer, self).__init__(parent, -1, style=wx.ALIGN_CENTRE)
        self.SetFont(wx.Font(wx.FontInfo(15).Family(wx.FONTFAMILY_TELETYPE)))

    @staticmethod
    def print(matrix):
        return '\n'.join([''.join([c for c in row]) for row in matrix])

    def show(self, matrix):
        self.SetLabel(self.print(matrix))
