class Point:
    def __init__(self,x, y):
        self.X = x
        self.Y = y

    def __eq__(self, other):
        if self.X == other.X and self.Y == other.Y:
            return True
        return False

    def __ne__(self, other):
        if self.X != other.X or self.Y != other.Y:
            return True
        return False

def comp(x,y):
    if x == y:
        print("Equal True")
    else:
        print("Equal False")

    if x != y:
        print("Not equal True")
    else:
        print("Not equal False")
#1
p1 = Point(1, 2)
p2 = Point(3, 6)
comp(p1,p2)

#2
p1 = Point(0, 0)
p2 = Point(0, 0)
comp(p1,p2)

#3
p1 = Point(0, 10)
p2 = Point(0, 0)
comp(p1,p2)