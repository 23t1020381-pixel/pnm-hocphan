# Bài 13 - Tìm và sửa lỗi template

Cài đặt và chạy:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
flask --app app run --debug
```
Mở http://127.0.0.1:5000.

Bản này đã sửa lỗi để chạy được. Kiểm tra /post/1, /post/2 và /post/99. Khi debug lỗi template, kiểm tra tên biến, tên template, endpoint và thụt lề Jinja2.

Lệnh chạy bằng termiral:
cd C:\ma_nguon_mo\chuong_04\Bai13
py -m pip install -r requirements.txt
flask --app app run --debug