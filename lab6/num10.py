class Summator:
    def transform(self, n):
        return n

    def sum(self, N):
        Total = 0
        for i in range(1, N + 1):
            Total += self.transform(i)
        return Total

class SquareSummator(Summator):
    def transform(self, n):
        return n ** 2

class CubeSummator(Summator):
    def transform(self, n):
        return n ** 3

N = 10
# Проверка 1
s1 = Summator()
result1 = s1.sum(N)
formula1 = N * (N + 1) // 2
print(f"Summator: {result1}, Формула: {formula1}")

# Проверка 2
s2 = SquareSummator()
result2 = s2.sum(N)
formula2 = N * (N + 1) * (2 * N + 1) // 6
print(f"SquareSummator: {result2}, Формула: {formula2}")

# Проверка 3
s3 = CubeSummator()
result3 = s3.sum(N)
formula3 = (N * (N + 1) // 2) ** 2
print(f"CubeSummator: {result3}, Формула: {formula3}")