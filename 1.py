A = int(input())
n = A//5
count = 0
for i in range(n):
    if (A-(5*(n-i)))%3 == 0:
        print((n-i)+(A-(5*(n-i)))//3)
        count += 1
        break
    elif A%3 == 0:
        print(A//3)
        count += 1
        break
if count == 0:
    print(-1)