n = [1, 3, 2, 5, 4, 2]
c = [0 for i in range(len(n))]
for j in n:
    c[j] += 1

for k in range(1, len(n)):
    c[k] += c[k-1]

d = [0 for l in range(len(n))]
for m in n:
    d[c[m]-1] = m
    c[m] -= 1
# print(c)
print(d)