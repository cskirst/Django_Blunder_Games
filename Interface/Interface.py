from .controller import Controller


class Interface:
    def __init__(self):
        self.c = Controller()

    def process(self, s, user):
        if s is not None:
            #commandList = s.split()
            print(s)
            return self.c.check(s, user)