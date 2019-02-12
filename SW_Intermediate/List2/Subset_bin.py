s = {-7, -3, -2, 5, 8}
list_1 = []
for i in range(1 << len(s)):
    list_2 = []
    for j in range(len(s)):
        if i & (1 << j):
            list_2.append(list(s)[j])
    
    list_1.append(list_2)

list_3 = []
for q in list_1:
    if sum(q) == 0 and q != []:
        list_3.append(q)

print(list_3)