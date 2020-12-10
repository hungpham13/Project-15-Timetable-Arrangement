from ortools.sat.python import cp_model
def input(FileName,toPrint):
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

FileName= 'data.txt'
n,m,T,S,G,D_G,C = input(FileName)
so_buoi,so_tiet= 10,6
all_gv = range(len(D_G))
all_p = range(m)
all_b = range(so_buoi)
all_t = range(so_tiet)
all_l = range(n)

###################
#CP a.k.a or-tools#
###################

model = cp_model.CpModel()
lc = {}
for l in all_l:
    for p in all_p:
        for b in all_b:
            for t in all_t:
                lc[(l, p, b, t)] = model.NewBoolVar('lc_l%ip%ib%it%i' %(l, p, b, t))

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
def or_tools():
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



Count = [0]*n # dùng để chỉ những lớp chưa xếp và đã xếp được bao nhiêu tiết
starting = [] # kết quả (lớp học lúc nào ở đâu)
lc={} # biến lựa chọn
# generating lc
for l in all_l:
	for p in all_p:
		for b in all_b:
			for t in all_t:
				lc[(l,p,b,t)]=0
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
        for p in all_p:
            for b in all_b:
                for t in all_t:
                    status = check_candidate(k,p,b,t)
                    if status != False: #Nếu status là False thì sẽ không sửa biến lựa chọn
                        lc[(k,p,b,t)] = 1
                        if status == 'First': #Nếu status là 'First'(lần đầu xếp lớp) thì lưu vào starting chỉ tg bắt đầu học
                            starting.append((k,p,b,t))
        Backtrack(k+1)
    if k == n:
        print_sol()
Backtrack(0)

def Bactracking(lc, remaining_classses):
    if not remaining_classses:
        return lc
    if satisfied_constraints(lc):
        next = remaining_classses.pop()
        for p in all_p:
            for b in all_b:
                for t in all_t:
                    lc_next = lc[:]
                    lc_next[(next,p,b,t)] = 1
                    next_state = Bactracking(lc_next, remaining_classses)
                    if next_state: return next_state
    return False

def satisfied_constraints(lc):
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


#Constraint 3 - Hung
def valid_list(l_S,pivot):
    '''list do dai >= 1, chua cac S_i'''
    if sum(l_S) == 0: return True
    has_pivot = False
    for i in range(len(l_S)):
        if l_S[i] == pivot:
            has_pivot = True
    if not has_pivot:
        return False

    up = True
    for i in range(len(l_S)):
        if i != 0 and l_S[i] + l_S[i-1] != 0:
            if up and l_S[i] != l_S[i-1] + 1: return False
            if not up and l_S[i] != l_S[i-1] - 1: return False
        if l_S[i] == pivot:
            up = False
    return True
def continuous(l,p,b):
    #tiet phai lien nhau
    l_S = []
    for i in range(7-T[l]):
        S_i = sum(lc[(l,p,b,t)] for t in range(i,i+T[l]))
        l_S.append(S_i)
        print(l_S)
    return valid_list(l_S,T[l])

# def enough(l):

#             if S == T[l]: pivot += 1
#             elif S == 0: zero += 1
#     if pivot == 1 and zero == len(all_p)*len(all_b) - 1:
#         return True
#     else:
#         return False

for l in all_l:
    for p in all_p:
        for b in all_b:
            periods = sum(lc[(l,p,b,t)] for t in all_t)
            model.Add(periods == T[l] or periods == 0)
    # for p in all_p:
    #     for b in all_b:
    #         continuous(l,p,b)
for b in all_b:
    print('Buoi',b)
    for t in all_t:
        print('-Tiet',t)
        for l in all_l:
            for p in all_p:
                if solver.Value(lc[(l,p,b,t)]) == 1:
                    print('--Lop',l,'hoc giao vien',G[l],'tai phong',p)
