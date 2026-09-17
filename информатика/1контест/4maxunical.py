numbers = list(map(int, input().split()))

while True:
    mx = max(numbers)
    position = []
    for i, x in enumerate(numbers):
        if x == mx:
            position.append(i)

    if len(position) == 1:
        print(mx)
        break
    for i in sorted(position, reverse = True):
        numbers.pop(i)
