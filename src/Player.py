class Player:
    events = []
    char = '@'
    inventory = {'food': 10}

    def update(self):
        while self.events:
            event = self.events.pop()
            self.handle_event(event)
        return []

    def handle_event(self, event):
        pass
