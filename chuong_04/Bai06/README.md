# Bài 6 - Bình luận và XSS

Cài đặt và chạy:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
flask --app app run --debug
```
Mở http://127.0.0.1:5000.

Không dùng {{ c.content|safe }} với nội dung người dùng nhập. Autoescape mặc định giúp hiển thị chuỗi HTML như văn bản, giảm nguy cơ XSS.

Lệnh chạy bằng termiral:
cd C:\ma_nguon_mo\chuong_04\Bai06
py -m pip install -r requirements.txt
flask --app app run --debug
