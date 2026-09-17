str = input().split()
N = int(str[0])
M = int(str[1])
K = int(str[2])
Ta = float(str[3])
Tb = float(str[4])
Tc = float(str[5])

if abs(N - K) * Ta + Ta * abs(N-M) + Tb*3 <= Tc * abs(N-M):
    print("elevator")
else:
    print("stairs")    