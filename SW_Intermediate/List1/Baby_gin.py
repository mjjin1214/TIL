n = list(map(int, input().split()))

def bg(n):
    ln = sorted(list(set(n)))
    sl3 = set()
    if len(ln) == 1:
        return True
    elif len(ln) == 2:
        if n.count(ln[0]) == 3:
            return True
    elif len(ln) == 3:
        for i in range(3):
            sl3.add(n.count(ln[i]))
        if (3 not in sl3) and (ln[0]+2 == ln[1]+1 == ln[2]):
            return True
    elif len(ln) == 4:
        for j in range(3):
            if n.count(ln[j]) == 3:
                ln.remove(ln[j])
                if (ln[0]+2 == ln[1]+1 == ln[2]):
                    return True
    elif (ln[0]+2 == ln[1]+1 == ln[2]) and (ln[3]+2 == ln[4]+1 == ln[5]):
        return True
    return False
print(bg(n))