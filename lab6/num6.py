class SparseArray:
    def __init__(self):
        self.Data = {}

    def __setitem__(self, i, value):
        if value != 0:
            self.Data[i] = value
        elif i in self.Data:
            del self.Data[i]

    def __getitem__(self, i):
        return self.Data.get(i, 0)

# Пример 1
arr = SparseArray()
arr[1] = 10
arr[8] = 20
for i in range(10):
    print('arr[{}] = {}'.format(i, arr[i]))

# Пример 2
print()
arr = SparseArray()
arr[10] = 123
arr[8] = 1
for i in range(8, 13):
    print('arr[{}] = {}'.format(i, arr[i]))

# Пример 3
print()
def print_elem(Array, Ind):
    print('arr[{}] = {}'.format(Ind, Array[Ind]))

arr = SparseArray()
index = 1000000000
arr[index] = 123
print_elem(arr, index - 1)
print_elem(arr, index)
print_elem(arr, index + 1)