def kon(n):
    k = 0
    while n > 0:
        k += n % 10
        n //= 10

    if k > 9:
        return kon(k)
    return k

n = int(input())
print(kon(n))