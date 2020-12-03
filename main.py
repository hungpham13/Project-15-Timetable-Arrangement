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

#CP a.k.a or-tools

model = cp_model.CpModel()
lc = {}
for l in all_l:
    for p in all_p:
        for b in all_b:
            for t in all_t:
                lc[(l, p, b, t)] = model.NewBoolVar('lc_l%ip%ib%it%i' %(l, p, b, t))


#Constraint 1,2

for b in all_b:
    for t in all_t:
        for g in range(D_G):
            model.Add(sum(sum(lc[(l,p,b,t)] for p in range(all_p)) \
                          for l in D_G[g]) <= 1)           #2b
        for p in all_p:
            model.Add(sum(lc[(l,p,b,t)] for l in all_l) <= 1) #2a
            for l in all_l:
                if S[l] > C[p]:
                    model.Add(lc[(l,p,b,t)] == 0)       #1

#Constraint 3 - Vu
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
                if S[c]<C[c]:
                    model.Add(lc[l,p,b,t] == 0) # chỗ không đủ thì không được xếp vào

#Constraint 3 - Hung
for l in all_l:
    for t in all_t:
        model.Add(sum(sum(lc[(l,p,b,t)] for p in all_p) for b in all_b) <=1) #3a


def valid_list(l_S,pivot):
    '''list do dai >= 1, chua cac S_i'''
    if set(l_S) == {0}: return True
    if pivot not in l_S: return False
    up = True
    for i in range(len(l_S)):
        if i != 0 and l_S[i] + l_S[i-1] != 0:
            if up and l_S[i] != l_S[i-1] + 1: return False
            if not up and l_S[i] != l_S[i-1] - 1: return False
        if l_S[i] == pivot:
            up = False
    return True

def continuous(l,p,b):
    l_S = []
    for i in range(6-T[l]):
        S_i = sum(lc[(l,p,b,t)] for t in range(i,i+T[l]))
        l_S.append(S_i)
    return valid_list(l_S,T[l])

for l in all_l:
    for p in all_p:
        for b in all_b:
            model.Add(continuous(l,p,b))
