a = int(input())
for i in range(a):
    print(f'#{i+1}', end=' ')
    b = []
    count = 0
    for j in range(9):
        b.append(list(map(int, input().split())))
        if sum(b[j]) != 45:
            count += 1
    if count != 0:
        print(0)
    else:
        for k in range(9):
            c = 0
            for l in range(9):
                c += b[l][k]
            if c != 45:
                print(0)
                count += 1
                break
        if count == 0:
            for m in range(0, 7, 3):
                for n in range(0, 7, 3):
                    c = 0
                    for o in range(3):
                        for p in range(3):
                            c += b[m+o][n+p]
                    if c != 45:
                        count += 1
                        break
            if count == 0:
                print(1)
            else:
                print(0)