import math

class MathFunction:
    def evaluate(self, x):
        raise NotImplementedError

class IdentityFunction(MathFunction):
    def evaluate(self, x):
        return x

class SqrtFunction(MathFunction):
    def evaluate(self, x):
        return math.sqrt(x)

class ConstantFunction(MathFunction):
    def __init__(self, value):
        self.value = value

    def evaluate(self, x):
        return self.value

class CompositeFunction(MathFunction):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def evaluate(self, x):
        left_val = self.left.evaluate(x) if isinstance(self.left, MathFunction) else self.left
        right_val = self.right.evaluate(x) if isinstance(self.right, MathFunction) else self.right

        if self.operator == '+':
            return left_val + right_val
        elif self.operator == '-':
            return left_val - right_val
        elif self.operator == '*':
            return left_val * right_val
        elif self.operator == '/':
            return left_val / right_val

functions = {
    'x': IdentityFunction(),
    'sqrt_fun': SqrtFunction()
}

def format_value(val):
    if abs(val - round(val)) < 1e-7:
        return str(int(round(val)))
    else:
        formatted = f"{val:.7f}".rstrip('0').rstrip('.')
        return formatted

num_commands = int(input())

for _ in range(num_commands):
    line = input().split()

    if line[0] == 'define':
        func_name = line[1]
        left_operand = line[2]
        operator = line[3]
        right_operand = line[4]

        if left_operand.replace('.', '').replace('-', '').isdigit():
            left = float(left_operand) if '.' in left_operand else int(left_operand)
            left = ConstantFunction(left)
        else:
            left = functions[left_operand]

        if right_operand.replace('.', '').replace('-', '').isdigit():
            right = float(right_operand) if '.' in right_operand else int(right_operand)
            right = ConstantFunction(right)
        else:
            right = functions[right_operand]

        functions[func_name] = CompositeFunction(left, operator, right)

    elif line[0] == 'calculate':
        func_name = line[1]
        points = list(map(float, line[2:]))

        func = functions[func_name]
        results = []

        for point in points:
            result = func.evaluate(point)
            results.append(format_value(result))

        print(' '.join(results))