lunch = {
    '중국집':'02-123-123',
    '양식집':'054-123-123',
}

dinner = dict(중국집='02-123-123')

lunch['분식집'] = '053-123-123'

print(lunch['중국집'])

for key in lunch:
    print(key)
    print(lunch[key])

idol = {
    'bts': {
        '지민':24,
        'RM':25
    }
}
idol['bts']['RM']

for key in lunch.keys():
    print(key)

for value in lunch.values():
    print(value)

for key, value in lunch.items():
    print(key, value)

#문제
score = {
    '수학':80,
    '국어':90,
    '음악':100
}

total = 0
for value in score.values():
    total += value
print(total/len(score))

print(sum(score.values())/len(score))

