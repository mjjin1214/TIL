a = int(input())
for i in range(a):
    b = 0
    for j in range(int(input())):
        b = b + ((-1)**(j))*(j+1)
    print(f'#{i+1} {b}')