from abc import ABC


class WidgetABC(ABC):
    def __init__(self, psready):
        self.psready = psready
        self.root = self.psready.root

    def place(self):
        pass

    def config(self):
        pass
