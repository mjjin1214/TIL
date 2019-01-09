t = int(input())
c = ['A+', 'A0', 'A-', 'B+', 'B0', 'B-', 'C+', 'C0', 'C-', 'D']
for l in range(t):
    n, k = map(int, input().split())
    b = []
    d = {}
    for i in range(n):
        a = list(map(int, input().split()))
        b.append(a[0]*0.35 + a[1]*0.45 + a[2]*0.2)
    e = sorted(b)
    for j in range(len(e)):
        d[e[j]] = c[9-int(j//(n/10))]
    print(f'#{l+1} {d[b[k-1]]}')