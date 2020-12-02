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

def enforce_class(L, P, B, T):
    for p in all_p:
        for b in all_b:
            for t in all_t:
                if (p,b,t)==(P,B,T):
                    if p <= P+classes_len[C]: # nếu mà nó nằm trong khoảng số tiết của lớp đó
                        return lc[(L,b,p,t)] == 1
                    else: # nếu mà nó nằm ngoài khoảng số tiết của lớp đó mà giông p,b,t
                        return lc[(L,b,p,t)] == 0
                else: # khác p,b,t thì không được
                    return return lc[(L,b,p,t)] == 0
for l in all_l:
    for p in all_p:
        for b in all_b:
            for t in all_t:
                model.Add(enforce_class(l,p,b,t)).OnlyEnforceIf(lc[(l,p,b,t)]) # chỉ thêm constraint nếu mà biến lc[l,p,b,t]==1 
