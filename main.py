from ortools.sat.python import cp_model
from copy import deepcopy
from random import randint

def input(FileName):
    f = open(FileName,'r')
    global so_lop, so_phong, so_buoi, so_tiet, T,S,G,D_G,C
    so_buoi, so_tiet= 10, 6
    so_lop, so_phong =  (int(i) for i in f.readline().split())
    T,S,G,D_G,C = [],[],[],{},[]
    for l in range(so_lop):
        tiet, gv, so_hs = (int(i) for i in f.readline().split())
        for X, y in zip((T,G,S),(tiet,gv,so_hs)):
            X.append(y)
        if gv in D_G:
            D_G[gv].append(l)
        else:
            D_G[gv] = [l]
    C = [int(i) for i in f.readline().split()]


FileName= 'data.txt'
input(FileName)
all_p = [p for p in range(m)]
all_b = range(so_buoi)
all_t = range(so_tiet)
all_l = [l for l in range(n)]

def randomize_data(FileName):
    rnum_hsmax = 0
    f = open(FileName, "w")
    n, m = randint(5, 25), randint(2, 5) #random số lớp (5-25) và số phòng (2-5)
    f.write(str(n) + ' ' + str(m) + '\n')
    for l in range(n):
        rnum_hs = randint(30, 50) #random số học sinh (30-50)
        f.write(str(randint(1, 6)) + ' ' + str(randint(1, 5)) + ' ' + str(rnum_hs) + '\n') #random độ dài (1-6) và giáo viên (1-5), học sinh rồi viết vào file 
        if rnum_hs > rnum_hsmax: #đảm bảo là luôn có phòng chứa được lớp nhiều học sinh nhất
            rnum_hsmax = rnum_hs
    room = ''
    for i in range(m - 1):
        room += str(randint(30, 50)) + ' ' #random số chỗ của m-1 phòng (30-50)
    f.write(room + str(rnum_hsmax))#viết vào file số chỗ của m-1 phòng và phòng cuối (Phòng cuối sẽ luôn có số chỗ bằng số lớp nhiều học sinh nhất)


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
###################
#CP a.k.a or-tools#
###################


# sol. printer TBD               
class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, lc, n, m, so_buoi, so_tiet, so_loi_giai):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._lc = lc
        self._l = n
        self._p = m
        self._so_buoi = so_buoi
        self._so_tiet = so_tiet
        self._so_loi_giai = so_loi_giai
        self._solution_count = 0


    def on_solution_callback(self):
        self._solution_count += 1
        if self._solution_count <= self._so_loi_giai:
            print('--------------loi giai %i----------------' % self._solution_count)
            Class=[]
            for b in range(self._so_buoi):
                for p in range(self._p):
                    for t in range(self._so_tiet):
                        for l in range(self._l):
                            if self.Value(self._lc[(l,p,b,t)]):
                                if l not in Class:
                                    ngay ,buoi = ngay_va_buoi(b)
                                    print('Class', l+1 ,'starts on', ngay, buoi, 'period', t+1, 'at room ', p+1, 'with teacher', G[l]+1 )
                                    Class.append(l)

    def solution_count(self):
        return self._solution_count
#end printer

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
    global model
    model = cp_model.CpModel()
    generate_decision_var('o')
    add_constraints()
    #Start solving and printing sols            
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    so_loi_giai = 1
    solution_printer = SolutionPrinter(lc, so_lop, so_phong, so_buoi, so_tiet, so_loi_giai)
    solver.SearchForAllSolutions(model, solution_printer)
    print(status)
    print('Statistics')
    print('  - conflicts       : %i' % solver.NumConflicts())
    print('  - branches        : %i' % solver.NumBranches())
    print('  - wall time       : %f s' % solver.WallTime())
    print('  - solutions found : %i' % solution_printer.solution_count())

# test_Ortools()

###########
#Heuristic#
###########


def print_sol(target):
    lop_da_duoc_xep = []
    final_target = 0
    for sp in starting:
        ngay,buoi = ngay_va_buoi(sp[2])
        print('Class', sp[0]+1 ,'starts on', ngay, buoi, 'period', sp[3]+1, 'at room ', sp[1]+1,'with teacher', G[sp[0]]+1)
        lop_da_duoc_xep.append(sp[0])
        if target == 'P': #ưu tiên xếp tiết #period
            final_target += T[sp[0]]
        if target == 'LT': #ưu tiên xếp số học sinh*tiết #learning time
            final_target += LT[sp[0]]
        if target == 'S': #ưu tiên xếp học sinh #Student
            final_target += S[sp[0]]
    print('The final target value is :', final_target)
    p = [i for i in all_l_h if i not in lop_da_duoc_xep]
    for l in p:
        print('Unable to place class ', p, 'in the timetable due to limiting rooms and conflicting schedule')


def check_candidate(l1,p1,b1,t1):
    global Count
    if Count[l1]>0 and Count[l1]<T[l1] :    #các tiết đặt sau lần đầu sẽ được xếp liền nhau
        Count[l1]+=1
        return True
    else:   #các tiết xếp lần đầu sẽ phải thỏa mãn các constraint
        if Count [l1] >= T[l1]: # ko xếp thừa tiết
            return False
        if t1 + T[l1] > so_tiet:# đảm bảo đủ chỗ để xếp tiết (nếu lớp có 5 tiết thì không được bắt đầu ở tiết thứ 2) 
            return False
        if S[l1] > C[p1]:
            return False #cons 1 #phòng thiếu chỗ sẽ không được xếp vào
        for l in all_l:
            if lc[(l,p1,b1,t1)] == 1: #cons 2 a #1 phòng chỉ chứa 1 lớp
                return False
        if G[l] == G[l1]:
            for p in all_p:
                if lc[(l,p,b1,t1)] == 1: #cons 2 b #1 gv chỉ dạy 1 lớp
                    return False
        Count[l1]+=1
        return 'First'


def Heuristic():
    global starting
    for l in all_l_h:
        placement(l)


def placement(k):
    for p in all_p_h:
        for b in all_b:
            for t in all_t:
                status = check_candidate(k,p,b,t)
                if status != False: #Nếu status là False thì sẽ không sửa biến lựa chọn
                    lc[(k,p,b,t)] = 1
                    if status == 'First': #Nếu status là 'First'(lần đầu xếp lớp) thì lưu vào starting chỉ tg bắt đầu học
                        starting.append((k,p,b,t))
                if Count[k] >= T[k]:
                    return


def HeuristicStart(target):
    global all_l_h, all_p_h, LT
    all_p_h = sort_list(all_p, C)
    if target == 'P': #ưu tiên xếp tiết #period
        all_l_h = sort_list(all_l, T)
        Heuristic()
    if target == 'LT': #ưu tiên xếp số học sinh*tiết #learning time
        LT = [T[i]*S[i] for i in range(n)]
        all_l_h = sort_list(all_l, LT)
        Heuristic()
    if target == 'S': #ưu tiên xếp học sinh #Student
        all_l_h = sort_list(all_l, S)
        Heuristic()

def TestHeuristic(target):
    generate_decision_var('h')
    HeuristicStart(target)
    print_sol(target)
#TestHeuristic('LT')
###########
#Backtrack#
###########

def Backtracking(lc, rmp, rmc):
    '''at first: rmc (remaining_classses) = so_lop
                 rmp = remain_periods '''
    if satisfied_c2b(lc, range(rmc,so_lop)): #Constraint 2b
        if not rmc:
            return lc
        l = rmc - 1
        for p in all_p:
            for b in all_b:
                if T[l] <= rmp[p][b] and S[l] <= C[p]: #c 3,1 and 2a
                    lc_copy, rmp_copy = deepcopy(lc), deepcopy(rmp)
                    start = so_tiet - rmp[p][b]
                    for t in range(start, start + T[l]):
                        lc_copy[(l,p,b,t)] = 1
                    rmp_copy[p][b] -= T[l]
                    next = Backtracking(lc_copy, rmp_copy, rmc - 1)
                    if next: return next
    return False

def satisfied_c2b(lc,all_l):
    '''all_l: not all classes, just classes which are arranged'''
    for b in all_b:
        for t in all_t:
            for g in D_G:
                if sum(sum(lc[(l,p,b,t)] for p in all_p) for l in D_G[g]) > 1:
                    return False
    return True

def test_Backtracking():
    generate_decision_var('b')
    result = Backtracking(lc, remain_periods, so_lop)
    if not result:
        print("Can't arrange")
    else:
        print_solution(result,'b')

def print_solution(lc, algo):
    for b in all_b:
        print('Buoi',b)
        for p in all_p:
            print('-Phong',p)
            for l in all_l:
                for t in all_t:
                    if lc[(l,p,b,t)] == 1:
                        print('--Lop',l,'hoc giao vien',G[l],'tiet',t)
# test_Backtracking()
