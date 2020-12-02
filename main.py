FileName= 'data.txt'
def input(FileName):
    """"""

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




