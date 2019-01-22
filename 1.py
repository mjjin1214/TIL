def only(x):
    a = []
    for i in x:
        if i not in a:
            a.append(i)
    return a

print(only([12,24,35,24,88,120,155,88,120,155]))