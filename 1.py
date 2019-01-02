import sys
a = list(range(1, int(sys.stdin.readline())+1))
for i in a:
    b = list(map(int, list(str(i))))
    if len(b) >= 3:
        if b[0]-b[1] != b[1]-b[2]:
            a.remove(a[i-1])
print(len(a))