n = int(input())
numbers  = []
for i in range(n):
    numbers.append(int(input()))

natural = []
negative = []

for num in numbers:
    if num >= 0:
        natural.append(num)
    else:
        negative.append(num)

natural.sort()
negative.sort(reverse = True)   

result = natural + negative
print( ' '.join(map(str,result)))