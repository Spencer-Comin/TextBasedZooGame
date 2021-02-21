import Event


class Warehouse:
    priceList = {
        'food': 10,
        'lion': 500,
        'tiger': 600,
        'zebra': 300,
        'camel': 300,
        'moose': 250,
        'giraffe': 400,
        'buffalo': 400,
        'penguin': 20,
        'yak': 450,
        'jaguar': 1000
    }
    sellDiscount = 0.8

    def __init__(self, inside_method, player):
        pass
        self._insideMethod = inside_method
        self.emit = player.emit
        self.player = player

    @property
    def player_inside(self):
        return self._insideMethod()

    def buy(self, amount=1, obj=''):
        if not obj:
            # flip stuff around
            obj = amount
            amount = 1
        if not self.valid_number(amount):
            self.notify(f'cannot buy {amount} things')
            return
        if self.player_inside:
            if obj in self.priceList:
                cost = amount * self.priceList[obj]
                if cost <= self.player.inventory['money']:
                    self.player.add_to_inventory(obj, amount)
                    self.player.remove_from_inventory('money', cost)
                    self.notify(f'bought {amount} {obj} for ${cost}')
                else:
                    self.notify(f"you don't have enough money to get {amount} {obj}")
            else:
                self.notify(f'{obj} not available in warehouse')
        else:
            self.notify('cannot buy anything because you are not in the warehouse')

    def sell(self, amount=1, obj=''):
        if not obj:
            # flip stuff around
            obj = amount
            amount = 1
        if not self.valid_number(amount):
            self.notify(f'cannot sell {amount} things')
            return
        if self.player_inside:
            if obj in self.player.inventory and obj in self.priceList:
                if self.player.inventory[obj] >= amount:
                    cost = amount * self.priceList[obj] * self.sellDiscount
                    self.player.remove_from_inventory(obj, amount)
                    self.player.add_to_inventory('money', cost)
                    self.notify(f'sold {amount} {obj} for ${cost}')
                else:
                    self.notify(f"you don't have {amount} {obj}")
            else:
                self.notify(f'{obj} not in inventory')
        else:
            self.notify('cannot sell anything because you are not in the warehouse')

    @staticmethod
    def valid_number(number):
        return number >= 1

    def notify(self, message):
        self.emit(Event.Event(details={'notification': message}))
