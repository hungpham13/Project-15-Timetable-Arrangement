from ortools.sat.python import cp_model
from random import randint

def input(FileName):
    f = open(FileName,'r')
    (n, m) =  (int(i) for i in f.readline().split())
    T,S,G,D_G,C = [],[],[],[],[]
    for c in range(n):
        [so_tiet, gv, so_hs] = (int(i) for i in f.readline().split())
        T.append(so_tiet)
        S.append(so_hs)
        G.append(gv)
        if len(D_G)<gv:
            D_G.append([c])
        else:
            D_G[gv-1].append(c)
    C = [int(i) for i in f.readline().split()]
    return (n,m,T,S,G,D_G,C)

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


FileName= 'data.txt'
n,m,T,S,G,D_G,C = input(FileName)
so_buoi,so_tiet= 10,6
all_gv = range(len(D_G))
all_p = range(m)
all_b = range(so_buoi)
all_t = range(so_tiet)
all_l = range(n)

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
        Count = [0 for i in range(n)] # dùng để chỉ những lớp chưa xếp và đã xếp được bao nhiêu tiết
        starting = [] # kết quả (lớp học lúc nào ở đâu)

###################
#CP a.k.a or-tools#
###################

model = cp_model.CpModel()

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
            print('loi giai %i' % self._solution_count)
            for b in range(self._so_buoi):
                print('Buoi',b)
                for p in range(self._p):
                    for t in range(self._so_tiet):
                        for l in range(self._l):
                            if self.Value(self._lc[(l,p,b,t)]):
                                print('Lop',l,'hoc phong',p,'tiet',t)

    def solution_count(self):
        return self._solution_count
#end printer

def or_tools():
    #Constraint 1,2
    for b in all_b:
        for t in all_t:
            for g in all_gv:
                model.Add(sum(sum(lc[(l,p,b,t)] for p in all_p) \
                              for l in D_G[g]) <= 1)           #2b
            for p in all_p:
                model.Add(sum(lc[(l,p,b,t)] for l in all_l) <= 1) #2a
                for l in all_l:
                    if S[l] > C[p]:
                        model.Add(lc[(l,p,b,t)] == 0)       #1

    #Constraint 3 - Vu
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

    #Start solving and printing sols            
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    so_loi_giai = 1
    solution_printer = SolutionPrinter(lc, n, m, so_buoi, so_tiet, so_loi_giai)
    solver.SearchForAllSolutions(model, solution_printer)
    print(status)
    print('Statistics')
    print('  - conflicts       : %i' % solver.NumConflicts())
    print('  - branches        : %i' % solver.NumBranches())
    print('  - wall time       : %f s' % solver.WallTime())
    print('  - solutions found : %i' % solution_printer.solution_count())


###########
#Backtrack#
###########
def ngay_va_buoi(k): #lấy ngày và buổi từ k
    ngay = ['Monday','Tuesday','Wednesday','Thursday','Friday']
    buoi = ['Morning','Afternoon']
    return(ngay[k//2],buoi[k%2])
def print_sol():
    for sp in starting:
        ngay,buoi = ngay_va_buoi(sp[2])
        print('Class', sp[0]+1 ,'starts on', ngay, buoi, 'period', sp[3]+1, 'at room ', sp[1]+1)
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
def Backtrack(k):
    global starting
    if k < n:
        placement(k)
        Backtrack(k+1)
    if k == n:
        print_sol()
def placement(k):
    for p in all_p:
        for b in all_b:
            for t in all_t:
                status = check_candidate(k,p,b,t)
                if status != False: #Nếu status là False thì sẽ không sửa biến lựa chọn
                    lc[(k,p,b,t)] = 1
                    if status == 'First': #Nếu status là 'First'(lần đầu xếp lớp) thì lưu vào starting chỉ tg bắt đầu học
                        starting.append((k,p,b,t))
                if Count[k] >= T[k]:
                    return
# Backtrack(0)

def Backtracking(lc, remaining_classses):
    if not remaining_classses:
        return lc
    print(satisfied_constraints(lc))
    if satisfied_constraints(lc):
        next = remaining_classses.pop()
        for p in all_p:
            for b in all_b:
                for t in all_t:
                    lc_next = dict(lc)
                    lc_next[(next,p,b,t)] = 1
                    next_state = Bactracking(lc_next, remaining_classses)
                    if next_state: return next_state
    return False

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
                            for b in all_b) \
               for p in all_p) != T[l]:  # 3a
            return False
        for p in all_p:
            for b in all_b:
                if sum(lc[(l,p,b,t)] for t in all_t) != 0:
                    l_S = [sum(lc[(l,p,b,t)] for t in range(i,i+T[l])) \
                           for i in range(7-T[l])]
                    if T[l] not in l_S: #3b
                        return False


#Constraint 3 - Hung
def test_Backtracking():
    generate_decision_var('b')
    global lc
    Backtracking(lc, all_l)
    for b in all_b:
        print('Buoi',b)
        for t in all_t:
            print('-Tiet',t)
            for l in all_l:
                for p in all_p:
                    if lc[(l,p,b,t)] == 1:
                        print('--Lop',l,'hoc giao vien',G[l],'tai phong',p)
test_Backtracking()
