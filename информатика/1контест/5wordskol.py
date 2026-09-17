from collections import Counter

words = input().split()
counts = Counter(words)

pairs = list(counts.items())

to_sort = []
for word, freq in pairs:
    key = (-freq, word)
    to_sort.append((key, word, freq))

to_sort.sort()

ordered = []
for key, word, freq in to_sort:
    ordered.append((word, freq))

for word, freq in ordered:
    print(freq, word)    