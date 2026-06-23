def main():
    print("Номер 1")
    N1()
    print("\nНомер 2")
    N2()
    print("\nНомер 3")
    N3()
    print("\nНомер 4")
    N4()
    print("\nНомер 5")
    N5()
    print("\nНомер 6")
    N6()
    print("\nНомер 7")
    N7()
    print("\nНомер 8")
    N8()
    print("\nНомер 9")
    N9()
    print("\nНомер 10")
    N10()
    print("\nНомер 11")
    N11()
    print("\nНомер 12")
    N12()
    print("\nНомер 13")
    N13()
    print("\nНомер 14")
    N14()
    print("\nНомер 15")
    N15()

def N1():
    s = input()
    print(s[2])
    print(s[-2])
    print(s[:5])
    print(s[:-2])
    print(s[::2])
    print(s[1::2])
    print(s[::-1])
    print(s[::-2])
    print(len(s))

def N2():
    s = input()
    mid = (len(s) + 1) // 2
    result = s[mid:] + s[:mid]
    print(result)

def N3():
    s = input()
    result = s[:s.find('h') + 1] + s[s.find('h') + 1:s.rfind('h')][::-1] + s[s.rfind('h'):]
    print(result)

def N4():
    s = input()
    first = s.find('f')
    last = s.rfind('f')

    if first != -1 and first == last:
        print(first)
    elif first != last and first != -1:
        print(first, last)

def N5():
    word1 = input()
    while 1:
        word2 = input()
        if word1[-1] == word2[0]:
            word1 = word2
        else:
            print(word2)
            break

def N6():
    s = input()
    a = ''
    for i in range(len(s)):
        a += s[i] * (i + 1)
    print(a)

def N7():
    s = input()
    a=0
    for i in range(len(s)):
        match s[i]:
            case s:
                a=1

def N8():
    s = input()
    n = len(s)

    if n % 2 == 0:
        mid = n // 2
        for i in range(mid):
            space = ' ' * (mid - i - 1)
            if i == 0:
                print(space+ s[mid - 1] + ' ' + s[mid])
            else:
                left = s[mid - 1 - i]
                right = s[mid + i]
                hole = ' ' * (2 * i+1)
                print(space + left + hole + right)
    else:
        mid = n // 2
        for i in range(mid + 1):
            spaces = ' ' * (mid - i)
            if i == 0:
                print(spaces + s[mid])
            else:
                left = s[mid - i]
                right = s[mid + i]
                hole = ' ' * (2 * i - 1)
                print(spaces + left + hole + right)

def N9():
    lst = list(map(int, input().split()))
    for i in range(1, len(lst)):
        if lst[i] > lst[i-1]:
            print(lst[i], end=' ')

def N10():
    lst = list(map(int, input().split()))
    for i in range(len(lst) - 1):
        if (lst[i] > 0 and lst[i+1] > 0) or (lst[i] < 0 and lst[i+1] < 0):
            print(lst[i], lst[i+1])
            break

def N11():
    lst = input().split()
    for i in range(0, len(lst) - 1, 2):
        lst[i], lst[i+1] = lst[i+1], lst[i]
    print(' '.join(lst))

def N12():
    lst = input().split()
    for i in range(len(lst)):
        if lst.count(lst[i]) == 1:
            print(lst[i], end=' ')

def N13():
    indices = list(map(int, input().split()))
    s = input()
    words = s.split()
    result = []
    for idx in indices:
        result.append(words[idx-1])
    result[0] = result[0].capitalize()
    print(' '.join(result))

def N14():
    queens = []
    for _ in range(8):
        x, y = map(int, input().split())
        queens.append((x, y))

    for i in range(8):
        for j in range(i+1, 8):
            x1, y1 = queens[i]
            x2, y2 = queens[j]
            if x1 == x2 or y1 == y2 or abs(x1-x2) == abs(y1-y2):
                print('YES')
                return
    print('NO')

def N15():
    queue = []
    while(1):
        event = input()
        if 'последний-' in event:
            queue.append(event)
        elif 'спросить-' in event:
            queue.insert(0, event)
        elif event == 'следующий':
            if queue:
                print(f'Заходит {queue.pop(0)}!')
            else:
                print('В очереди никого нет.')
        else: print("Не верная команда\nпоследний-(имя)\nспросить-(имя)\nследующий ")

main()