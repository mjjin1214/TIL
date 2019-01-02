'''
문제 5.
표준 입력으로 물품 가격 여러 개가 문자열 한 줄로 입력되고, 각 가격은 ;(세미콜론)으로 구분되어 있습니다.
입력된 가격을 높은 가격순으로 출력하는 프로그램을 만드세요.
# 입력 예시: 300000;20000;10000
'''

prices = input('물품 가격을 입력하세요: ')
# 아래에 코드를 작성해 주세요.
a = prices.split(';')
#print(a)
#print(type(a))
#print(len(a))

int_a = []
for i in range(0, len(a)):
    int_a.append(a[i])
#print(int_a)
#print(type(int_a))

int_prices = []
for i in a:
    int_prices.append(int(i))

b = list(map(int, a))
#print(b)

int_a.sort(reverse=True)
sorted_price = sorted(int_prices, reverse=True)
b.sort(reverse=True)

print(int_a, sorted_price, b)