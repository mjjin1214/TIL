num = list(map(int, input().split()))
c = [0 for i in range(10)]
for j in num:
    c[j] += 1

k = t = r = 0
while k < 10:
    if c[k] >= 3:
        c[k] -= 3
        t += 1
        continue
    if c[k] >= 1 and c[k+1] >= 1 and c[k+2] >= 1:
        c[k] -= 1
        c[k+1] -= 1
        c[k+2] -= 1
        continue
    k += 1

if r + t == 2:
    print('Baby Gin')
else:
    print('Lose')