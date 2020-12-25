from ortools.sat.python import cp_model
from copy import deepcopy
import time, resource

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

def generate_decision_var(algo):
    ''' Generate descision variable base on specify algorithm
    algo: string - 'o': or-tools, 'b': backtracking, 'h': heuristic'''
    global lc
    lc = {}
    for l in all_l:
        for p in all_p:
            for b in all_b:
                for t in all_t:
                    if algo == 'o':
                        lc[(l, p, b, t)] = model.NewBoolVar('lc_l%ip%ib%it%i' %(l, p, b, t))
                    else:
                        lc[(l,p,b,t)]=0
    if algo == 'h':
        global Count, starting
        Count = [0 for i in all_l] # dùng để chỉ những lớp chưa xếp và đã xếp được bao nhiêu tiết
        starting = [] # kết quả (lớp học lúc nào ở đâu)
    if algo == 'b':
        global remain_periods
        remain_periods = [[so_tiet for b in all_b] for p in all_p]

def ngay_va_buoi(k): #lấy ngày và buổi từ k
    ngay = ['Monday','Tuesday','Wednesday','Thursday','Friday']
    buoi = ['Morning','Afternoon']
    return(ngay[k//2],buoi[k%2])

def print_solution(lc):
    for b in all_b:
        print('Buoi',b+1,' '.join(ngay_va_buoi(b)))
        for p in all_p:
            print('----Phong %i: %i cho' %(p+1,C[p]))
            for l in all_l:
                periods = ' '.join(str(t+1) for t in all_t if lc[(l,p,b,t)] == 1)
                if periods:
                    print('-------------Lop %i: %i hoc sinh, giao vien %i, tiet %s' %(l+1,S[l],G[l],periods))
            print('\n')
        print('\n','\n')

###################
#CP a.k.a or-tools#
###################

def add_constraints():
    #Constraint 1,2
    for b in all_b:
        for t in all_t:
            for g in D_G:
                model.Add(sum(sum(lc[(l,p,b,t)] for p in all_p) \
                                                for l in D_G[g]) <= 1)           #2b
            for p in all_p:
                model.Add(sum(lc[(l,p,b,t)] for l in all_l) <= 1) #2a
                for l in all_l:
                    if S[l] > C[p]:
                        model.Add(lc[(l,p,b,t)] == 0)       #1

    #Constraint 3
    def continuous(l, p, b):
        if T[l] == 6:
            return sum(lc[(l, p, b, t)] for t in all_t) == 6
        if T[l] == 5:
            return sum(lc[(l, p, b, t)] for t in range(0, 5)) == 5 or \
                   sum(lc[(l, p, b, t)] for t in range(1, 6)) == 5
        if T[l] == 4 :
            return sum(lc[(l, p, b, t)] for t in range(0, 4)) == 4 or \
                   sum(lc[(l, p, b, t)] for t in range(1, 5)) == 4 or \
                   sum(lc[(l, p, b, t)] for t in range(2, 6)) == 4
        if T[l] == 3:
            return sum(lc[(l, p, b, t)] for t in range(0, 3)) == 3 or \
                   sum(lc[(l, p, b, t)] for t in range(1, 4)) == 3 or \
                   sum(lc[(l, p, b, t)] for t in range(2, 5)) == 3 or \
                   sum(lc[(l, p, b, t)] for t in range(3, 6)) == 3
        if T[l] == 2:
            return sum(lc[(l, p, b, t)] for t in range(0, 2)) == 2 or \
                   sum(lc[(l, p, b, t)] for t in range(1, 3)) == 2 or \
                   sum(lc[(l, p, b, t)] for t in range(2, 4)) == 2 or \
                   sum(lc[(l, p, b, t)] for t in range(3, 5)) == 2 or \
                   sum(lc[(l, p, b, t)] for t in range(4, 6)) == 2
        if T[l] == 1:
            return sum(lc[(l, p, b, t)] for t in all_t) == 1


    for l in all_l:
        model.Add(sum(sum(sum(lc[(l, p, b, t)] for t in all_t) \
                            for b in all_b) \
                            for p in all_p) == T[l])  # đủ số tiết của lớp
        for p in all_p:
            for b in all_b:
               for t in all_t:
                    model.Add(continuous(l,p,b)).OnlyEnforceIf(lc[(l,p,b,t)]) #3b

def test_Ortools():
    global model,solver
    model = cp_model.CpModel()
    generate_decision_var('o')
    add_constraints()
    #Start solving and printing sols
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    result = {}
    for i in lc:
        result[i] = solver.Value(lc[i])
    if status == 4: #optimal
        print_solution(result)
    else:
        print('Cannot place all class due to limiting rooms and/or conflicting schedule')
    return result


###########
#Heuristic#
###########

def check_candidate(l1,p1,b1,t1):
    if t1 + T[l1] >6:# đảm bảo đủ chỗ để xếp tiết (nếu lớp có 5 tiết thì không được bắt đầu ở tiết thứ 2) 
        return False
    if S[l1] > C[p1]:
        return False #cons 1 #phòng thiếu chỗ sẽ không được xếp vào
    for t in range(t1, t1+T[l1]):#kiểm tra các tiết tiếp theo sau t1
        for l in all_l_h:#các lớp còn lại
            if lc[(l,p1,b1,t)] == 1: #cons 2 a #1 phòng chỉ chứa 1 lớp
                return False
            if G[l] == G[l1]:
                for p in all_p:
                    if lc[(l,p,b1,t)] == 1: #cons 2 b #1 gv chỉ dạy 1 lớp
                        return False
    return True


def Heuristic():
    for l in all_l_h:
        placement(l)


def placement(k):
    for p in all_p_h:
        for b in all_b:
            for t in all_t:
                status = check_candidate(k,p,b,t)
                if status != False: #Nếu status là False thì sẽ không sửa biến lựa chọn
                    for t1 in range(t, t+T[k]):
                        lc[(k,p,b,t1)]=1
                    return


def HeuristicStart(target):
    generate_decision_var('h')
    global all_l_h, all_p_h
    all_p_h = sorted(all_p,key = lambda x:C[x])
    if target == 'P': #ưu tiên xếp tiết #period
        all_l_h = sorted(all_l,key = lambda x: T[x])
    if target == 'LT': #ưu tiên xếp số học sinh*tiết #learning time
        all_l_h = sorted(all_l,key = lambda x:T[x]*S[x])
    if target == 'S': #ưu tiên xếp học sinh #Student
        all_l_h = sorted(all_l,key = lambda x:S[x])
    Heuristic()
    return lc

def TestHeuristic():
    best_result, max_arranged_p = 0,0
    list_of_targets = ('P','LT','S')
    for target in list_of_targets:
        lc = HeuristicStart(target)
        arranged_periods = sum(lc.values())
        if arranged_periods > max_arranged_p:
            best_result, best_target,max_arranged_p = lc,target,arranged_periods
    print('Heuristic with target',best_target)
    print_solution(best_result)
    return best_result

###########
#Backtrack#
###########

def Backtracking(lc, rmp, rmc):
    '''at first: rmc (remaining_classses) = so lop con lai
                 rmp = remain_periods '''
    if not rmc:
        return lc
    l = rmc - 1
    for b in all_b:
        for p in all_p:
            if satisfy_constraints(l,b,p,rmp[p][b],lc):
                lc_copy, rmp_copy = deepcopy(lc), deepcopy(rmp)
                taking_t = range(so_tiet - rmp[p][b], so_tiet - rmp[p][b] + T[l])
                for t in taking_t:
                    lc_copy[(l,p,b,t)] = 1
                rmp_copy[p][b] -= T[l]
                next = Backtracking(lc_copy, rmp_copy, rmc - 1)
                if next: return next
    return False

def satisfy_constraints(l0,b0,p0,periods_left,lc):
    if T[l0] > periods_left or S[l0] > C[p0]: #1,2a,3
        return False
    start_t = so_tiet - periods_left
    for t in range(start_t, start_t + T[l0]): #taking_t
        for p in all_p:
            for l in range(l0+1, so_lop): #taken_l
                if lc[(l,p,b0,t)] == 1 and G[l0] == G[l]: #2b
                    return False
    return True

def test_Backtracking():
    generate_decision_var('b')
    result = Backtracking(lc, remain_periods, so_lop)
    if not result:
        print("Can't arrange")
    else:
        print_solution(result)
    return result



#############
# DEBUGGING #
#############

def right(lc):
    for b in all_b:
        for t in all_t:
            for g in D_G:
                if sum(sum(lc[(l,p,b,t)] for p in all_p) for l in D_G[g]) > 1: #2b
                    print('Teacher %i teaches more than 1 class in session %i, period %i' %(g,b+1,t+1))
                    yield ('2b')
            for p in all_p:
                if sum(lc[(l,p,b,t)] for l in all_l) > 1: #2a
                    print('Room %i take more than 1 classes in session %i, period %i' %(p+1,b+1,t+1))
                    yield ('2a')
                for l in all_l:
                    if S[l] > C[p] and lc[(l,p,b,t)] != 0: #1
                        print("Room %i can't contains class %i, not enough seats" %(p+1,l+1))
                        yield ('1')
    for l in all_l:
        taken_t = sum(sum(sum(lc[(l, p, b, t)] for t in all_t) for b in all_b) for p in all_p)
        if taken_t != T[l]:  # 3a
            print('Class %i take %i periods, it should take %i periods' %(l+1,taken_t,T[l]))
            yield ('3a')
        for p in all_p:
            for b in all_b:
                if sum(lc[(l,p,b,t)] for t in all_t) != 0:
                    l_S = [sum(lc[(l,p,b,t)] for t in range(i,i+T[l])) \
                           for i in range(7-T[l])]
                    if T[l] not in l_S: #3b
                        print('The periods class %i taken in sessions %i, room %i are not adjacent' %(l+1,b+1,p+1))
                        yield ('3b')

def check_solution(testFunction):
    print('Start checking....')
    start_time = time.time()
    lc = testFunction()
    print("---Time: %s seconds ---" % (time.time() - start_time))
    status = set(right(lc))
    if not status:
        print('Optimal solution')
    else:
        print('Not optimal, violate constraint: '+ ' '.join(status))
    print("Total memory usage:",resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)

FileName= 'data4.txt'
Input(FileName)
check_solution(test_Ortools)
