import os

p = os.getcwd() + '\\sprites\\' + 'plr1' + '\\' + 'in_attack' + '\\' + 'crouch'
for i in os.listdir(p):
    if '.txt' in i and 'info' not in i:
        print('sos')
        f = open(p + '\\' + i, 'r')
        st = f.read().split()
        f.close()
        f = open(p + '\\' + i, 'w')
        f.flush()
        f.write(' '.join([str(int(st[0]) - 10), str(int(st[1]) - 10), str(int(st[2]) + 20), str(int(st[3]))]))
        f.close()
