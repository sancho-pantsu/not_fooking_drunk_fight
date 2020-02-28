import os

p = os.getcwd() + '\\sprites\\' + 'plr1' + '\\' + 'in_attack'
for i in os.listdir(p):
    if '.txt' in i and 'info' not in i:
        f = open(p + '\\' + i, 'r')
        st = f.read().split()
        f.close()
        f = open(p + '\\' + i, 'w')
        f.flush()
        f.write(' '.join([str(int(st[0])), str(int(st[1])), str(int(st[2])), str(int(st[3]))]))
        f.close()
