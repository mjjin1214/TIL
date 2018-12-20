string = []
while True:
    input_data = input()
    if input_data == '':
        break
    else:
        string.append(input_data)

for line in string:
    print(line)