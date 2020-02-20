n = int(input())
s = {0: 1}
c = 0
mx = 0
for i in input():
    if i == '+':
        c += 1
    else:
        c -= 1
    if c in s:
        s[c] += 1
    else:
        s[c] = 1
    if c > mx:
        mx = c
print(s[mx])
