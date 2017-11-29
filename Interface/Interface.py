from .controller import Controller


class Interface:
    def __init__(self):
        self.c = Controller()

    def process(self, s):
        self.c.check(s)