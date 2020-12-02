def input(FileName):
    f = open(FileName,'r')
    (n, m) =  (int(i) for i in f.readline().split())
    T,S,G,D_G,C = [],[],[],[],[]
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
    return (n,m,T,S,G,D_G,C)

FileName= 'data.txt'
n,m,T,S,G,D_G,C = input(FileName)
so_buoi,so_tiet= 10,6
all_gv = range(len(D_G))
all_p = range(m)
all_b = range(so_buoi)
all_t = range(so_tiet)
all_l = range(n)
print(T,S,G,D_G)

for b in all_b:
    for t in all_t:
        for g in range(D_G):
            model.Add(sum(sum(lc[(l,p,b,t)] for p in range(all_p)) \
                          for l in D_G[g]) <= 1)           #2b
        for p in all_p:
            model.Add(sum(lc[(l,p,b,t)] for l in all_l)) #2a
            for l in all_l:
                if S[l] > C[p]:
                    model.Add(lc[(l,p,b,t)] == 1)       #1
