#Input
f = open(r'data.txt','r')
(n, m) =  (int(i) for i in f.readline().split())
T = []
S = []
G = []
D_G = []
for c in range(n):
    [so_tiet, gv, so_luong_hs] = (int(i) for i in f.readline().split())
    T.append(so_tiet)
    S.append(so_luong_hs)
    G.append(gv)
    if len(D_G)<gv:
        D_G.append([c])
    else:
        D_G[gv-1].append(c)
C = [int(i) for i in f.readline().split()]
so_gv = len(D_G)
so_buoi = 10
so_tiet = 6
all_gv = list(range(so_gv))
all_p = list(range(m))
all_n = list(range(so_buoi))
all_t = list(range(so_tiet))
all_l = list(range(n))
