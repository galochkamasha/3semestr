n = int(input())
def nanonacci(num):
    if num<=8:
        return 0
    if num == 9:
        return 1
    f = [0]*9
    f[8] = 1

    for i in range(10,n+1):
        next_num = sum(f)
        f.pop(0)
        f.append(next_num)

    return f[-1]
print( nanonacci(n))