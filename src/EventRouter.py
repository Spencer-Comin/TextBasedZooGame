from collections import defaultdict


class EventRouter:
    events = []
    listeners = defaultdict(list)

    def add_listener(self, listener, affect_type):
        self.listeners[affect_type].append(listener)

    def add_event(self, event):
        self.events.append(event)

    def get_emitter(self):
        return self.add_event

    def send_events(self):
        events_to_handle = self.events.copy()
        self.events.clear()
        while events_to_handle:
            event = events_to_handle.pop()
            for affect_type in event.affectees:
                for listener in self.listeners[affect_type]:
                    listener.handle_event(event)
