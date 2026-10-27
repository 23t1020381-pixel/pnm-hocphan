from flask import Flask, render_template, request

app = Flask(__name__)


# ==================== BÀI 1: MÁY TÍNH CƠ BẢN ====================
def chuyen_so(gia_tri):
    gia_tri = gia_tri.strip()
    if not gia_tri:
        raise ValueError("Vui lòng nhập một số.")
    if "," in gia_tri and "." in gia_tri:
        raise ValueError("Vui lòng chỉ dùng dấu phẩy hoặc dấu chấm thập phân.")
    try:
        return float(gia_tri.replace(",", "."))
    except ValueError:
        raise ValueError("Vui lòng nhập một số hợp lệ.")


def dinh_dang_so(so):
    if so.is_integer():
        return str(int(so))
    return f"{so:.10g}"


# ==================== BÀI 2: TÍNH ĐIỂM HỌC PHẦN ====================
def kiem_tra_diem(value, ten_o):
    val = str(value).strip() if value is not None else ""
    if val == "":
        return "Trống"
    val = val.replace(",", ".")
    try:
        num = float(val)
    except ValueError:
        return f"Lỗi ô {ten_o}: Vui lòng nhập một số."
    if num < 0 or num > 10:
        return f"Lỗi ô {ten_o}: Điểm phải từ 0 đến 10."
    return num


# ==================== BÀI 3: TÍNH CHỈ SỐ BMI ====================
def kiem_tra_bmi(cao_str, nang_str):
    c_val = str(cao_str).strip() if cao_str is not None else ""
    n_val = str(nang_str).strip() if nang_str is not None else ""

    loi_cao, loi_nang = None, None
    num_cao, num_nang = None, None

    # Kiểm tra chiều cao
    if not c_val:
        loi_cao = "Trống"
    else:
        c_clean = c_val.replace(",", ".")
        try:
            num_cao = float(c_clean)
            if num_cao < 50 or num_cao > 250:
                if 0 < num_cao < 50:
                    loi_cao = "Giá trị phải từ 50 đến 250. (nhập mét thay vì cm)"
                else:
                    loi_cao = "Lỗi ô chiều cao: Giá trị phải từ 50 đến 250."
        except ValueError:
            loi_cao = "Lỗi ô chiều cao: Vui lòng nhập một số."

    # Kiểm tra cân nặng
    if not n_val:
        loi_nang = "Trống"
    else:
        n_clean = n_val.replace(",", ".")
        try:
            num_nang = float(n_clean)
            if num_nang < 10 or num_nang > 300:
                loi_nang = "Lỗi ô cân nặng: Giá trị phải từ 10 đến 300."
        except ValueError:
            loi_nang = "Lỗi ô cân nặng: Vui lòng nhập một số."

    # Trả về kết quả kiểm tra
    if loi_cao == "Trống" and loi_nang == "Trống":
        return "Lỗi cả hai ô", None, None
    if loi_cao:
        return loi_cao, None, None
    if loi_nang:
        return loi_nang, None, None

    return None, num_cao, num_nang


# ==================== ROUTE CHÍNH ====================
@app.route("/", methods=["GET", "POST"])
def index():
    # Nhận bài toán được chọn (Mặc định: '1')
    bai = request.values.get("bai", "1")

    # Khởi tạo biến Bài 1
    a, b, op = "", "", "+"
    loi_a, loi_b, loi_op, ket_qua_1 = "", "", "", ""

    # Khởi tạo biến Bài 2
    cc, gk, ck = "", "", ""
    thong_bao_2 = ""

    # Khởi tạo biến Bài 3
    cao, nang = "", ""
    thong_bao_3, mau_3 = "", "success"

    if request.method == "POST":
        # --- BÀI 1 ---
        if bai == "1":
            a = request.form.get("a", "")
            b = request.form.get("b", "")
            op = request.form.get("op", "+")

            if op not in ["+", "-", "*", "/"]:
                loi_op = "Phép toán không hợp lệ."

            try:
                so_a = chuyen_so(a)
            except ValueError as e:
                loi_a = str(e)
                so_a = None

            try:
                so_b = chuyen_so(b)
            except ValueError as e:
                loi_b = str(e)
                so_b = None

            if not loi_a and not loi_b and not loi_op:
                if op == "+":
                    kq = so_a + so_b
                elif op == "-":
                    kq = so_a - so_b
                elif op == "*":
                    kq = so_a * so_b
                else:
                    if so_b == 0:
                        loi_b = "Không thể chia cho 0."
                        kq = None
                    else:
                        kq = so_a / so_b

                if kq is not None:
                    ket_qua_1 = f"{dinh_dang_so(so_a)} {op} {dinh_dang_so(so_b)} = {dinh_dang_so(kq)}"

        # --- BÀI 2 ---
        elif bai == "2":
            cc = request.form.get("cc", "")
            gk = request.form.get("gk", "")
            ck = request.form.get("ck", "")

            res_cc = kiem_tra_diem(cc, "CC")
            res_gk = kiem_tra_diem(gk, "GK")
            res_ck = kiem_tra_diem(ck, "CK")

            loi = []
            if isinstance(res_cc, str):
                loi.append(res_cc)
            if isinstance(res_gk, str):
                loi.append(res_gk)
            if isinstance(res_ck, str):
                loi.append(res_ck)

            if (
                len(loi) == 3
                and res_cc == "Trống"
                and res_gk == "Trống"
                and res_ck == "Trống"
            ):
                thong_bao_2 = "Lỗi cả 3 ô"
            elif len(loi) > 0:
                thong_bao_2 = loi[0]
            else:
                diem_hp = round(res_cc * 0.1 + res_gk * 0.3 + res_ck * 0.6, 1)

                if res_ck < 1.0:
                    diem_chu = "F (điểm thi dưới 1)"
                elif diem_hp >= 8.5:
                    diem_chu = "A"
                elif diem_hp >= 7.0:
                    diem_chu = "B"
                elif diem_hp >= 5.5:
                    diem_chu = "C"
                elif diem_hp >= 4.0:
                    diem_chu = "D"
                else:
                    diem_chu = "F"

                thong_bao_2 = f"{diem_hp} · {diem_chu}"

        # --- BÀI 3 ---
        elif bai == "3":
            cao = request.form.get("cao", "")
            nang = request.form.get("nang", "")

            err, val_cao, val_nang = kiem_tra_bmi(cao, nang)

            if err:
                thong_bao_3 = err
                mau_3 = "error-box"
            else:
                cao_m = val_cao / 100.0
                bmi = round(val_nang / (cao_m**2), 1)

                # Cân nặng nên có (ứng với BMI 18.5 - 22.9)
                min_weight = round(18.5 * (cao_m**2), 1)
                max_weight = round(22.9 * (cao_m**2), 1)

                # Phân loại theo chuẩn Châu Á
                if bmi < 18.5:
                    phan_loai = "Thiếu cân (vàng)"
                    mau_3 = "warning"
                elif bmi < 23.0:
                    phan_loai = "Bình thường (xanh)"
                    mau_3 = "success"
                elif bmi < 25.0:
                    phan_loai = "Thừa cân (vàng)"
                    mau_3 = "warning"
                else:
                    phan_loai = "Béo phì (đỏ)"
                    mau_3 = "danger"

                # Ghép kết quả hiển thị
                if 18.5 <= bmi < 23.0:
                    thong_bao_3 = f"{bmi} · {phan_loai}; nên có {min_weight} – {max_weight} kg"
                else:
                    thong_bao_3 = f"{bmi} · {phan_loai}"

    return render_template(
        "index.html",
        bai=bai,
        a=a,
        b=b,
        op=op,
        loi_a=loi_a,
        loi_b=loi_b,
        loi_op=loi_op,
        ket_qua_1=ket_qua_1,
        cc=cc,
        gk=gk,
        ck=ck,
        thong_bao_2=thong_bao_2,
        cao=cao,
        nang=nang,
        thong_bao_3=thong_bao_3,
        mau_3=mau_3,
    )


if __name__ == "__main__":
    app.run(debug=True)