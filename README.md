# Project-15
## Nội dung :
Có N lớp 1,2,..., N cần được xếp thời khóa biểu. Mỗi lớp i có t(i) là số tiết và g(i) là giáo viên đã được phân công dạy lớp đó và s(i) là số sinh viên của lớp 
Có M phòng học 1, 2, ..., M, trong đó c(i) là số chỗ ngồi của phòng i  Trong tuần có 5 ngày (từ thứ 2 đến thứ 5), mỗi ngày chia thành 12 tiết (6 tiết sáng và 6 tiết chiều).  
Hãy lập thời khóa biểu (xác định ngày, tiết và phòng gán cho mỗi lớp)  
Hai lớp có chung giáo viên thì phải xếp thời khóa biểu tách rời nhau  
Số sinh viên trong mỗi lớp phải nhỏ hơn hoặc bằng số chỗ ngồi của phòng học

## Dữ liệu đầu vào :
Input  
Dòng 1: ghi N và M 
Dòng i+1 (i = 1,…, N): ghi t(i), g(i) và s(i)  
Dòng N+2: ghi c(1), c(2), …, c(M)

## Phân tích bài toán : Với mỗi lớp:
Gọi T = [] : lưu số tiết của N lớp, n phần tử
Gọi G = [] : lưu mã giáo viên, nhập vào
Gọi S = [] : lưu số học sinh của N lớp, n phần tử
Gọi Sh = [] : đánh dấu tiết bắt đầu học bắt đầu của
Gọi D = [] : số ngày học trong tuần
Gọi Shift = []: Số tiết trong ngày
