import sys
n = int(sys.stdin.readline())
a = n/3

k = 0
while a > 1:
    a //= 2
    k += 1
print(f'k={k}')

len_b = 5
for i in range(k):
    len_b = (len_b)*2+1
print(f'len_b={len_b}')
# for i in range(k):
#     len_b = (2*(len_b[i])+1)
# print(f'len_b={len_b}')

def star(n):
    if n == 1:
        print(' '*int(((len_b-5)/2)), end='')
        print('  *  ', end='')
    else:
        star(n-1)
        print('\n'+' '*int((len_b-5-(6*((n-1)//3)))/2), end='')
        if n%3 == 1:
            print('  *  ', end='')
        elif n%3 == 2:
            print(' * * ', end='')
        else:
            print('*****', end='')

        if (n-1)//3 >= 1:
            print(' '*((n-1)//3), end ='')
            if n%3 == 1:
                print('  *  ', end='')
            elif n%3 == 2:
                print(' * * ', end='')
            else:
                print('*****', end='')
star(n)