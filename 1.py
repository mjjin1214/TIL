def z(b, c, d):
    ct = 0
    for i in range(b):
        a = d[i].split('0')
        for k in a:
            if len(k) == c:
                ct += 1
    return ct

a = int(input())
for i in range(a):
    b, c = map(int, input().split())
    d = []
    count = 0
    for j in range(b):
        d.append(input().replace(' ', ''))
    count += z(b, c, d)
    # for j in range(b):
    #     d.append(input().replace(' ', ''))
    #     e = d[j].split('0')
    #     for k in e:
    #         if len(k) == c:
    #             count += 1
    g = []
    for l in range(b):
        f = ''
        for m in range(b):
            f += d[m][l]
        g.append(f)
    count += z(b, c, g)
    # for n in g:
    #     h = n.split('0')
    #     for n in h:
    #         if len(n) == c:
    #             count += 1
    print(f'#{i+1} {count}')