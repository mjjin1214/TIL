city = {
    '서울':[-6, -10, 6],
    '대전':[-3, -6, 2],
    '광주':[-0, -2, 10],
    '구미':[2, -2, 9]
}

#for key in city.keys():
#    print(sum(city[key]), len(city[key]))

#for key in city.keys():
#    average = sum(city[key])/len(city[key])
#    print(f"{key}:{average}")

for k, v in city.items():
    total = 0
    count = 0
    for val in v:
        total += val
        count += 1
    print(f"{k}:{total/count}")

# for name, temp in city.items():
#     total_temp = 0
#     for t in temp
#         total_temp += t
#     avg_temp = total_temp / len(temp)
#     avg_temp = sum(temp) / len(temp)
#     print(f'{name} : {avg_temp}')