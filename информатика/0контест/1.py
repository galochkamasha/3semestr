a, b, c = map(int, input().split())
#.split разделяет по пробелам, input получает на вход
# map(int, ) map() применяет функцию int() к каждому эл-ту списка

print(max(a, b, c) - min(a, b, c))