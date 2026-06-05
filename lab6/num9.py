class Triangle:
    def __init__(self, a, b, c):
        self.SideA = a
        self.SideB = b
        self.SideC = c

    def perimeter(self):
        return self.SideA + self.SideB + self.SideC

class EquilateralTriangle(Triangle):
    def __init__(self, a):
        super().__init__(a, a, a)

Tri = Triangle(3,4,5)
print(Tri.perimeter())

ETri = EquilateralTriangle(3)
print(ETri.perimeter())