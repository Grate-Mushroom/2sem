def ConditionPositive(x):
    return x > 0

def ConditionAll(x):
    return True

def ConditionDivisibleBy5(x):
    return x % 5 == 0

def TransformMakeNegative(x):
    return x * -1

def TransformSquare(x):
    return x ** 2

def TransformIncrement(x):
    return x + 1

Commands = {
    'make_negative': (ConditionPositive, TransformMakeNegative),
    'square': (ConditionAll, TransformSquare),
    'strange_command': (ConditionDivisibleBy5, TransformIncrement)
}

Numbers = list(map(int, input().split()))
CountCommands = int(input())

for _ in range(CountCommands):
    CommandName = input().strip()

    if CommandName in Commands:
        Condition, Transformation = Commands[CommandName]

        for i in range(len(Numbers)):
            if Condition(Numbers[i]):
                Numbers[i] = Transformation(Numbers[i])

print(*Numbers)