import time, resource
from main import test_Backtracking,input
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

def check_solution(testFunction, data):
    input(data)
    print('Start checking....')
    start_time = time.time()
    lc = testFunction()
    print("---Time: %s seconds ---" % (time.time() - start_time))
    if satisfied_constraints(lc):
        print('Optimal solution')
    else:
        print('Not optimal')
    print("Total memory usage:",resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)

check_solution(test_Backtracking, 'data2.txt')
