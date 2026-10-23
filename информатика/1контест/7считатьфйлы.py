words = set()
for path in input().split():
    try:
        with open(path, encoding="utf-8") as f:
            words.update(f.read().split())
    except OSError:
        pass
print(*sorted(words))