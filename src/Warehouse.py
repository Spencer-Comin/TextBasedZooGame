class Warehouse:
    def __init__(self, inside_method):
        pass
        self._insideMethod = inside_method

    @property
    def player_inside(self):
        return self._insideMethod()
