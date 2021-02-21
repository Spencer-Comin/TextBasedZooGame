import wx
import Event


class InputHandler(wx.TextCtrl):
    def __init__(self, parent):
        super(InputHandler, self).__init__(parent, -1, style=wx.TE_PROCESS_ENTER)
        self.emitEvent = parent.game.eventRouter.add_event

        def handle_enter(e):
            self.emitEvent(Event.Event(Event.Type.COMMAND,
                                       details={'command': self.GetValue()}))
            self.Clear()

        self.Bind(wx.EVT_TEXT_ENTER, handle_enter)

        def handle_keypress(e):
            key_code = e.GetKeyCode()
            if key_code == wx.WXK_UP:
                self.emitEvent(Event.Event(Event.Type.MOVE_PLAYER,
                                           affects=(Event.AffecteesType.ZOO, Event.AffecteesType.PLAYER),
                                           details={'move': (-1, 0)}))
            elif key_code == wx.WXK_DOWN:
                self.emitEvent(Event.Event(Event.Type.MOVE_PLAYER,
                                           affects=(Event.AffecteesType.ZOO, Event.AffecteesType.PLAYER),
                                           details={'move': (1, 0)}))
            elif key_code == wx.WXK_RIGHT:
                self.emitEvent(Event.Event(Event.Type.MOVE_PLAYER,
                                           affects=(Event.AffecteesType.ZOO, Event.AffecteesType.PLAYER),
                                           details={'move': (0, 1)}))
            elif key_code == wx.WXK_LEFT:
                self.emitEvent(Event.Event(Event.Type.MOVE_PLAYER,
                                           affects=(Event.AffecteesType.ZOO, Event.AffecteesType.PLAYER),
                                           details={'move': (0, -1)}))
            else:
                e.Skip()

        self.Bind(wx.EVT_KEY_DOWN, handle_keypress)
