n = [1, 3, 2, 5, 4, 2]
c = [0 for i in range(min(n), max(n)+1)]
for j in n:
    c[j] += 1

print(c)