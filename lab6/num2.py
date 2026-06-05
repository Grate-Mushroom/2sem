class Balance:
    def __init__(self):
        self.LeftWeight = 0
        self.RightWeight = 0

    def add_right(self, w):
        self.RightWeight += w

    def add_left(self, w):
        self.LeftWeight += w

    def result(self):
        if self.LeftWeight == self.RightWeight:
            return '='
        elif self.RightWeight > self.LeftWeight:
            return 'R'
        else:
            return 'L'
balance = Balance()
balance.add_right(10)
balance.add_left(9)
balance.add_left(2)
print(balance.result())

balance = Balance()
balance.add_right(10)
balance.add_left(5)
balance.add_left(5)
print(balance.result())
balance.add_left(1)
print(balance.result())