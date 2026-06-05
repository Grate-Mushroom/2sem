class Selector:
    def __init__(self, values):
        self.Values = values

    def get_odds(self):
        return [x for x in self.Values if x % 2 != 0]

    def get_evens(self):
        return [x for x in self.Values if x % 2 == 0]

#1
values = [11, 12, 13, 14, 15, 16, 22, 44, 66]
selector = Selector(values)
odds = selector.get_odds()
evens = selector.get_evens()
print(' '.join(map(str, odds)))
print(' '.join(map(str, evens)))

#2
values = [6, 6, 8, 4, 8, 7, 6, 4, 7, 5]
selector = Selector(values)
odds = selector.get_odds()
evens = selector.get_evens()
print(' '.join(map(str, odds)))
print(' '.join(map(str, evens)))

#3
values = []
selector = Selector(values)
odds = selector.get_odds()
evens = selector.get_evens()
print(' '.join(map(str, odds)))
print(' '.join(map(str, evens)))