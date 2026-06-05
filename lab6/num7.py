class Polynomial:
    def __init__(self, coefficients):
        self.Coefficients = coefficients

    def __call__(self, x):
        result = 0
        for i in range(len(self.Coefficients)):
            result += self.Coefficients[i] * (x ** i)
        return result

    def __add__(self, other):
        len1 = len(self.Coefficients)
        len2 = len(other.Coefficients)
        max_len = max(len1, len2)
        new_coeffs = []

        for i in range(max_len):
            coeff1 = self.Coefficients[i] if i < len1 else 0
            coeff2 = other.Coefficients[i] if i < len2 else 0
            new_coeffs.append(coeff1 + coeff2)

        return Polynomial(new_coeffs)

# Пример 1
poly = Polynomial([10, -1])
print(poly(0))
print(poly(1))
print(poly(2))

# Пример 2
print()
poly1 = Polynomial([0, 0, 1])
print(poly1(-2))
print(poly1(-1))
print(poly1(0))
print(poly1(1))
print(poly1(2))
print()

poly2 = Polynomial([0, 0, 2])
print(poly2(-2))
print(poly2(-1))
print(poly2(0))
print(poly2(1))
print(poly2(2))
print()

poly3 = poly1 + poly2
print(poly3(-2))
print(poly3(-1))
print(poly3(0))
print(poly3(1))
print(poly3(2))
print()

# Пример 3
poly1 = Polynomial([0, 1])
poly2 = Polynomial([10])
poly3 = poly1 + poly2
poly4 = poly2 + poly1

print(poly3(-2), poly4(-2))
print(poly3(-1), poly4(-1))
print(poly3(0), poly4(0))
print(poly3(1), poly4(1))
print(poly3(2), poly4(2))