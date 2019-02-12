s = {-7, -3, -2, 5, 8}
li = []
t = [0 for r in range(len(s))]
for i in range(2):
    t[0] = i
    for j in range(2):
        t[1] = j
        for k in range(2):
            t[2] = k
            for l in range(2):
                t[3] = l
                for m in range(2):
                    t[4] = m
                    li.append(t[:])
print(li)
li2 = []
for n in li:
    t2 = []
    for o, p in zip(n, s):
        if o == 1:
            t2.append(p)
    if t2 != []:
        li2.append(set(t2))

li3 = []
for q in li2:
    if sum(q) == 0:
        li3.append(q)

print(li3)