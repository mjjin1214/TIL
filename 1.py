a = int(input())
b = []
for i in range(a):
    b.append(input())
    if not (1 <= int(b[i][4:6]) <= 12):
        print(f'#{i+1} -1')
    elif int(b[i][4:6]) in [1, 3, 5, 7, 8, 10, 12]:
        if not (1 <= int(b[i][6:8]) <= 31):
            print(f'#{i+1} -1')

        else:
            print(f'#{i+1} {b[i][0:4]}/{b[i][4:6]}/{b[i][6:8]}')
    elif int(b[i][4:6]) in [4, 6, 9, 11]:
        if not (1 <= int(b[i][6:8]) <= 30):
            print(f'#{i+1} -1')

        else:
            print(f'#{i+1} {b[i][0:4]}/{b[i][4:6]}/{b[i][6:8]}')
    else:
        if not (1 <= int(b[i][6:8]) <=28 ):
            print(f'#{i+1} -1')

        else:
            print(f'#{i+1} {b[i][0:4]}/{b[i][4:6]}/{b[i][6:8]}')