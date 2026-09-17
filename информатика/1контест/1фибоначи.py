n = int(input())

def fibonacci(num):
    prev = 0
    curr = 1
    for i in range(num - 1):
        prev, curr = curr, prev + curr
    return prev

print(fibonacci(n))