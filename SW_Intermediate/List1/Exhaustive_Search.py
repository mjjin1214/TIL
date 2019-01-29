n = input().split()
li = []
for i in range(6):
    for j in range(6):
        if j == i:
            continue
        for k in range(6):
            if k == i or k == j:
                continue
            for l in range(6):
                if l == i or l == j or l == k:
                    continue
                for m in range(6):
                    if m == i or m == j or m == k or m == l:
                        continue
                    for o in range(6):
                        if o != i and o != j and o != k and o != l and o != m:
                            li.append(f'{n[i]}{n[j]}{n[k]}{n[l]}{n[m]}{n[o]}')

print(li)