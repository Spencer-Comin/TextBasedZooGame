from collections import defaultdict
import Event


class Player:
    inventoryMax = 30
    char = '@'
    inventory = defaultdict(int)

    def __init__(self, emit):
        self.inventory.update({'food': 10, 'money': 1000})
        self.emit = emit

    def handle_event(self, event: Event.Event):
        if event.type is Event.Type.BALANCE_CHANGE:
            self.inventory['money'] += event.details['change']

    @property
    def inventory_size(self):
        return sum([count for item, count in self.inventory.items() if item != 'money'])

    def add_to_inventory(self, obj, amount):
        if amount + self.inventory_size <= self.inventoryMax:
            self.inventory[obj] += amount

