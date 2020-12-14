from random import randint

def randomize_data(FileName, n, m):
    rnum_hsmax = 0
    f = open(FileName, "w")
    f.write(str(n) + ' ' + str(m) + '\n')
    for l in range(n):
        rnum_hs = randint(30, 50) #random số học sinh (30-50)
        f.write(str(randint(1, 6)) + ' ' + str(randint(1, floor(n/8))) + ' ' + str(rnum_hs) + '\n') #random độ dài (1-6) và giáo viên (1-floor(n/8)), học sinh rồi viết vào file 
        if rnum_hs > rnum_hsmax: #đảm bảo là luôn có phòng chứa được lớp nhiều học sinh nhất
            rnum_hsmax = rnum_hs
    room = ''
    for i in range(m - 1):
        room += str(randint(30, 50)) + ' ' #random số chỗ của m-1 phòng (30-50)
    f.write(room + str(rnum_hsmax))#viết vào file số chỗ của m-1 phòng và phòng cuối (Phòng cuối sẽ luôn có số chỗ bằng số lớp nhiều học sinh nhất)
