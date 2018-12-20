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