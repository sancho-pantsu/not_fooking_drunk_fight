n, k = map(int, input().split())
d = [int(i) for i in input().split()]
res = n
for i in d:
    res -= n - i
if res > 0:
    print(res)
else:
    print(0)
