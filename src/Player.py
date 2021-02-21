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
        if event.type is Event.Type.ADD_TO_INVENTORY:
            self.add_to_inventory(event.asset, event.details['amount'])
        elif event.type is Event.Type.REMOVE_FROM_INVENTORY:
            self.remove_from_inventory(event.asset, event.details['amount'])

    @property
    def inventory_size(self):
        return sum([count for item, count in self.inventory.items() if item != 'money'])

    def add_to_inventory(self, obj, amount):
        if amount + self.inventory_size <= self.inventoryMax:
            self.inventory[obj] += amount
            return True
        return False

    def remove_from_inventory(self, obj, amount):
        self.inventory[obj] -= amount

