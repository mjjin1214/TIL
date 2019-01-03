import sys
n = int(sys.stdin.readline())
a = n/3

k = 0
while a > 1:
    a //= 2
    k += 1
print(f'k={k}')

len_b = [5]
for i in range(k):
    len_b.append(2*(len_b[i])+1)
print(f'len_b={len_b}')

def space(k):
    
    print(' '*int((len_b[1]-len_b[0])/2), end='')

count = 0
for i in range(n):
    if count == 0:
        space(k)
        print('  *  ')
        count +=1
    elif count == 1:
        space(k)
        print(' * * ')
        count += 1
    else:
        space(k)
        print('*****')
        count = 0
