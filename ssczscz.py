n = int(input())
children = [[False] * (n + 1) for _ in range(n + 1)]
parents = [[False] * (n + 1) for _ in range(n + 1)]
for i in range(n):
    for j in input().split():
        children[i][int(j)] = True
visited = [False] * (n + 1)

st = []
for i in range(1, n):
    if parents[i].count(True) == 0:
        st += [i]

for i in st:
    
