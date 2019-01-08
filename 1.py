t = int(input())
for i in range(t):
    n, m = map(int, input().split())
    a = []
    for j in range(n):
        a.append(list(map(int, input().split())))
    for k in range(n-m):

