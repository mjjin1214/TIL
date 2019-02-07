T = int(input())

for i in range(T):
    N = int(input())
    L = list(input())
    M = ''
    C = 0
    for j in reversed(L):
        if L.count(j) > C:
            M = j
            C = L.count(j)
    print(f'#{i+1} {M} {C}')
