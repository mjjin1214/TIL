a = int(input())
for i in range(a):
    b, c = map(int, input().split())
    d = c-b
    e = d**(1/2)
    f = int(e)
    if d == 0:
        print(d)
    elif e == f:
        print(f+f-1)
    elif d > f**2+f:
        print(f+f+1)
    else:
        print(f+f)