from Zoo import Zoo
from Player import Player
import Event
from Commands import CommandHandler
from EventRouter import EventRouter
from Warehouse import Warehouse


class Game:
    printer = None
    notifications = []

    def __init__(self, filename):
        self.eventRouter = EventRouter()
        emit_method = self.eventRouter.get_emitter()
        super().__init__()
        self.player = Player(emit_method)
        self.zoo = Zoo(filename, self.player.char, emit_method)
        self.commandHandler = CommandHandler(self.zoo, self.player, Warehouse(self.zoo.in_warehouse))
        self.eventRouter.add_listener(self.player, Event.AffecteesType.PLAYER)
        self.eventRouter.add_listener(self.zoo, Event.AffecteesType.ZOO)
        self.eventRouter.add_listener(self, Event.AffecteesType.PLAYER)
        self.eventRouter.add_listener(self, Event.AffecteesType.NONE)

    def set_notifications(self, notifications):
        self.notifications = notifications
        self.commandHandler.notificationsDump = notifications

    def update(self):
        self.zoo.update()
        self.eventRouter.send_events()
        self.printer.show(self.zoo.map)

    def handle_event(self, event):
        if 'command' in event.details:
            self.notifications.append(event.details['command'])
            self.commandHandler.execute(event.details['command'])
        if 'notification' in event.details:
            self.notifications.append(event.details['notification'])
