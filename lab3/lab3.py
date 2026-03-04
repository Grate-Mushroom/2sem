def main():
    N1()
    N2()
    N3()
    N4()
    N5()
    N6()
    N7()
    N8()
    N9()
    N10()

def N1():
    print(len(set(input("введите числа через пробел: ").split())), "различных чисел")

def N2():
    print(len(set(input("введите числа через пробел 1: ").split()) & set(input("введите числа через пробел 2: ").split())),"общих чисел")

def N3():
    print(*sorted(set(input("введите числа через пробел 1: ").split()) & set(input("введите числа через пробел 2: ").split())), "- общие числа по возрастанию")

def N4():
    nums = input().split()
    history = set()
    for n in nums:
        if n in history:
            print('YES')
        else:
            print('NO')
            history.add(n)

def N5():
    #там 17 слов. Я считал
    with open('num5.txt', 'r', encoding='utf-8') as f:
        n = int(f.readline())
        words = set()
        for _ in range(n):
            words.update(f.readline().split())
        print(len(words))

def N6():
    with open('num6.txt', 'r', encoding='utf-8') as f:
        n = int(f.readline().strip())
        counts = {}
        for _ in range(n):
            surname = f.readline().strip()
            counts[surname] = counts.get(surname, 0) + 1
        result = sum(c for c in counts.values() if c > 1)
        print(result)
def N7():
    text = input().split()
    counts = {}
    for w in text:
        print(counts.get(w, 0), end=' ')
        counts[w] = counts.get(w, 0) + 1

def N8():
    with open('num8.txt', 'r', encoding='utf-8') as f:
        n = int(f.readline().strip())
        synonyms = {}
        for _ in range(n):
            a, b = f.readline().split()
            synonyms[a] = b
            synonyms[b] = a
    print(f)
    word = input("Слово для синонима: ")
    print(synonyms[word])

def N9():
    with open('num9.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    n = int(lines[0].strip())
    votes = {}
    for i in range(1, n + 1):
        parts = lines[i].split()
        name = parts[0]
        count = int(parts[1])
        votes[name] = votes.get(name, 0) + count
    for name in sorted(votes.keys()):
        print(name, votes[name])

def N10():
    with open('num10.txt', 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    n = int(lines[0])
    permissions = {}
    idx = 1
    for _ in range(n):
        parts = lines[idx].split()
        filename = parts[0]
        ops = set(parts[1:])
        permissions[filename] = ops
        idx += 1

    m = int(lines[idx])
    idx += 1
    mapping = {'read': 'R', 'write': 'W', 'execute': 'X'}
    for _ in range(m):
        parts = lines[idx].split()
        op = parts[0]
        filename = parts[1]
        idx += 1
        if filename in permissions and mapping[op] in permissions[filename]:
            print("OK")
        else:
            print("Access denied")


main()
