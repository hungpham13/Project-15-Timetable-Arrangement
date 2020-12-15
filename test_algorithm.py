import time, resource
from main import test_Backtracking

def Input(FileName):
    f = open(FileName,'r')
    global so_lop, so_phong, so_buoi, so_tiet, T,S,G,D_G,C
    so_buoi, so_tiet= 10, 6
    so_lop, so_phong =  (int(i) for i in f.readline().split())
    T,S,G,D_G = [],[],[],{}
    for l in range(so_lop):
        tiet, gv, so_hs = (int(i) for i in f.readline().split())
        for X, y in zip((T,G,S),(tiet,gv,so_hs)):
            X.append(y)
        if gv in D_G:
            D_G[gv].append(l)
        else:
            D_G[gv] = [l]
    C = [int(i) for i in f.readline().split()]
    global all_p, all_b, all_t, all_l
    all_p = list(range(so_phong))
    all_b = range(so_buoi)
    all_t = range(so_tiet)
    all_l = list(range(so_lop))


FileName= 'data2.txt'
Input(FileName)

def satisfied_constraints(lc):
    for b in all_b:
        for t in all_t:
            for g in all_gv:
                if sum(sum(lc[(l,p,b,t)] for p in all_p) for l in D_G[g]) > 1: #2b
                    return False
            for p in all_p:
                if sum(lc[(l,p,b,t)] for l in all_l) > 1: #2a
                    return False
                for l in all_l:
                    if S[l] > C[p] and lc[(l,p,b,t)] != 0: #1
                        return False
    for l in all_l:
        if sum(sum(sum(lc[(l, p, b, t)] for t in all_t) \
               for b in all_b) for p in all_p) != T[l]:  # 3a
            return False
        for p in all_p:
            for b in all_b:
                if sum(lc[(l,p,b,t)] for t in all_t) != 0:
                    l_S = [sum(lc[(l,p,b,t)] for t in range(i,i+T[l])) \
                           for i in range(7-T[l])]
                    if T[l] not in l_S: #3b
                        return False
    return True

def check_solution(testFunction):
    print('Start checking....')
    start_time = time.time()
    lc = testFunction()
    print("---Time: %s seconds ---" % (time.time() - start_time))
    if satisfied_constraints(lc):
        print('Optimal solution')
    else:
        print('Not optimal')
    print("Total memory usage:",resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
check_solution(test_Backtracking)
