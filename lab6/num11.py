class Summator:
    def transform(self, n):
        return n

    def sum(self, N):
        Total = 0
        for i in range(1, N + 1):
            Total += self.transform(i)
        return Total

class PowerSummator(Summator):
    def __init__(self, b):
        self.Power = b

    def transform(self, n):
        return n ** self.Power

class SquareSummator(PowerSummator):
    def __init__(self):
        super().__init__(2)

class CubeSummator(PowerSummator):
    def __init__(self):
        super().__init__(3)

# Проверка
N = 5

# PowerSummator с степенью 2
ps = PowerSummator(2)
print(f"PowerSummator(2) = {ps.sum(N)}")

# PowerSummator с степенью 3
ps3 = PowerSummator(3)
print(f"PowerSummator(3) = {ps3.sum(N)}")

# SquareSummator
ss = SquareSummator()
print(f"SquareSummator = {ss.sum(N)}")

# CubeSummator
cs = CubeSummator()
print(f"CubeSummator = {cs.sum(N)}")