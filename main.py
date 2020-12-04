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


# sol. printer TBD               
class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, lc, n, m, so_buoi, so_tiet, so_loi_giai):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._lc = lc
        self._n = n
        self._m = m
        self._so_buoi = so_buoi
        self._so_tiet = so_tiet
        self._so_loi_giai = so_loi_giai
        self._solution_count = 0
        print('start')


    def on_solution_callback(self):
        self._solution_count += 1
        if self._solution_count <= self._so_loi_giai:
            print('loi giai %i' % self._solution_count)
            for p in range(self._m):
                for b in range(self._so_buoi):
                    for p in range(self._so_tiet):
                        for l in range(self._n):
                            if self.Value(self._lc[(l,p,b,t)]):
                                print(l,p,b,t)


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
def enforce_class(l1, p1, b1, t1):
    for p in all_p:
        for b in all_b:
            for t in all_t:
                if (p,b,t)==(p1,b1,t1):
                    if t+T[l1]>5:
                        return False
                    else:
                        if t <= t+T[l1]:     # nếu mà nó nằm trong khoảng số tiết của lớp đó
                            return lc[(l1,p,b,t)] == 1
                        else: # nếu mà nó nằm ngoài khoảng số tiết của lớp đó mà giông p,b,t
                                return lc[(l1,p,b,t)] == 0
                else: # khác p,b,t thì không được
                    return lc[(l1,p,b,t)] == 0

for l in all_l:
    for p in all_p:
        for b in all_b:
            for t in all_t:
                model.Add(enforce_class(l,p,b,t)).OnlyEnforceIf(lc[(l,p,b,t)]) # chỉ thêm constraint nếu mà biến lc[l,p,b,t]==1  
    model.Add(sum(sum(sum(lc[(l,p,b,t)] for t in all_t)\
                                        for b in all_b)\
                                        for p in all_p)==T[l]) # đủ số tiết của lớp

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
            model.Add(continuous(l,p,b)) #3b

#Start solving and printing sols            
solver = cp_model.CpSolver()
solver.parameters.linearization_level = 0
status = solver.Solve(model)
so_loi_giai = 1
solution_printer = SolutionPrinter(lc, n, m, so_buoi, so_tiet, so_loi_giai)
solver.SearchForAllSolutions(model, solution_printer)

# print()
# print('Statistics')
# print('  - conflicts       : %i' % solver.NumConflicts())
# print('  - branches        : %i' % solver.NumBranches())
# print('  - wall time       : %f s' % solver.WallTime())
# print('  - solutions found : %i' % solution_printer.solution_count())
