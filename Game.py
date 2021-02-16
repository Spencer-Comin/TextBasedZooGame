from Zoo import Zoo
from Player import Player
import Event
from Commands import CommandHandler


class Game:
    printer = None
    notifications = []

    def __init__(self, filename):
        super().__init__()
        self.player = Player()
        self.zoo = Zoo(filename, self.player.char)
        self.commandHandler = CommandHandler(self.zoo, self.player)
        self.events = []

    def set_notifications(self, notifications):
        self.notifications = notifications
        self.commandHandler.notificationsDump = notifications

    def update(self):
        self.printer.show(self.zoo.map)
        while self.events:
            event = self.events.pop()
            self.handle_event(event)
        self.events.extend(self.player.update())
        self.events.extend(self.zoo.update())

    def handle_event(self, event):
        if Event.AffecteesType.PLAYER in event.affectees:
            self.player.events.append(event)
            if 'notification' in event.details:
                self.notifications.append(event.details['notification'])
        if Event.AffecteesType.ZOO in event.affectees:
            self.zoo.events.append(event)
        if Event.AffecteesType.NONE in event.affectees:
            print(event)
            self.notifications.append(event.details.get('command', ''))
            self.commandHandler.execute(event.details.get('command', ''))
