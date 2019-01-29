def BubbleSort(n):
    for i in range(len(n)-1, -1, -1):
        for j in range(i):
            if n[j] > n[j+1]:
                n[j], n[j+1] = n[j+1], n[j]
    return n

print(BubbleSort([11, 33, 22, 55, 44]))