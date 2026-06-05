class ReversedList:
    def __init__(self, lst):
        self.Values = lst

    def __len__(self):
        return len(self.Values)

    def __getitem__(self, i):
        return self.Values[len(self.Values) - 1 - i]

# Пример 1
rl = ReversedList([10, 20, 30])
for i in range(len(rl)):
    print(rl[i])
print()
# Пример 2
rl = ReversedList([])
print(len(rl))
print()
# Пример 3
rl = ReversedList([10])
print(len(rl))
print(rl[0])