# Bài 2 - TemplateNotFound

Cài đặt và chạy:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
flask --app app run --debug
```
Mở http://127.0.0.1:5000.

Để tái hiện lỗi, đổi thành render_template('profle.html'). Sửa bằng cách kiểm tra chính tả tên file và đặt file trong thư mục templates/.

Lệnh chạy bằng termiral:
cd C:\ma_nguon_mo\chuong_04\Bai02
py -m pip install -r requirements.txt
flask --app app run --debug