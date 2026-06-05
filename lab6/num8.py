class Queue:
    def __init__(self, *values):
        self.Values = list(values)

    def append(self, *values):
        self.Values.extend(values)

    def copy(self):
        return Queue(*self.Values)

    def pop(self):
        if not self.Values:
            return None
        return self.Values.pop(0)

    def extend(self, queue):
        self.Values.extend(queue.Values)

    def next(self):
        if len(self.Values) <= 1:
            return Queue()
        return Queue(*self.Values[1:])

    def __add__(self, other):
        NewQueue = self.copy()
        NewQueue.extend(other)
        return NewQueue

    def __iadd__(self, other):
        self.extend(other)
        return self

    def __eq__(self, other):
        return self.Values == other.Values

    def __rshift__(self, n):
        if n >= len(self.Values):
            return Queue()
        return Queue(*self.Values[n:])

    def __str__(self):
        if not self.Values:
            return "[]"
        return "[" + " -> ".join(map(str, self.Values)) + "]"

    def __next__(self):
        return self.next()

q1 = Queue(1, 2, 3)
print(q1)
q1.append(4, 5)
print(q1)
qx = q1.copy()
print(qx.pop())
print(qx)
q2 = q1.copy()
print(q2)
print(q1 == q2, id(q1) == id(q2))
q3 = q2.next()
print(q1, q2, q3, sep='\n')
print(q1 + q3)
q3.extend(Queue(1, 2))
print(q3)
q4 = Queue(1, 2)
q4 += q3 >> 4
print(q4)
q5 = next(q4)
print(q4)
print(q5)