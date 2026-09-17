def is_correct(N, M, windows):
    K = len(windows)
    
    for i in range(K):
        x1, x2, y1, y2 = windows[i]
        
        if x1 < 0 or x2 > N or y1 < 0 or y2 > M:
            return False
        if x1 >= x2 or y1 >= y2:
            return False
        
        for j in range(i + 1, K):
            x3, x4, y3, y4 = windows[j]
            
            if max(x1, x3) < min(x2, x4) and max(y1, y3) < min(y2, y4):
                return False
    
    return True

N, M = map(int, input().split())
K = int(input())
windows = [tuple(map(int, input().split())) for _ in range(K)]

print("correct" if is_correct(N, M, windows) else "broken")