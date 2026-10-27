from flask import Flask, render_template, request

app = Flask(__name__)


def kiem_tra_bmi(cao_str, nang_str):
    c_val = str(cao_str).strip() if cao_str is not None else ""
    n_val = str(nang_str).strip() if nang_str is not None else ""

    loi_cao, loi_nang = None, None
    num_cao, num_nang = None, None

    # Kiểm tra chiều cao (cm)
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

    # Kiểm tra cân nặng (kg)
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

    # Xử lý trả về thông báo lỗi
    if loi_cao == "Trống" and loi_nang == "Trống":
        return "Lỗi cả hai ô", None, None
    if loi_cao:
        return loi_cao, None, None
    if loi_nang:
        return loi_nang, None, None

    return None, num_cao, num_nang


@app.route("/", methods=["GET", "POST"])
def index():
    cao = ""
    nang = ""
    thong_bao = ""
    mau_ket_qua = "success"

    if request.method == "POST":
        cao = request.form.get("cao", "")
        nang = request.form.get("nang", "")

        err, val_cao, val_nang = kiem_tra_bmi(cao, nang)

        if err:
            thong_bao = err
            mau_ket_qua = "error-box"
        else:
            # Chuyển chiều cao cm sang m để tính BMI = cân nặng / (chiều cao)^2
            cao_m = val_cao / 100.0
            bmi = round(val_nang / (cao_m**2), 1)

            # Cân nặng nên có (ứng với BMI 18.5 - 22.9)
            min_weight = round(18.5 * (cao_m**2), 1)
            max_weight = round(22.9 * (cao_m**2), 1)

            # Phân loại BMI theo chuẩn Châu Á
            if bmi < 18.5:
                phan_loai = "Thiếu cân (vàng)"
                mau_ket_qua = "warning"
            elif bmi < 23.0:
                phan_loai = "Bình thường (xanh)"
                mau_ket_qua = "success"
            elif bmi < 25.0:
                phan_loai = "Thừa cân (vàng)"
                mau_ket_qua = "warning"
            else:
                phan_loai = "Béo phì (đỏ)"
                mau_ket_qua = "danger"

            # Ghép chuỗi thông báo kết quả
            if 18.5 <= bmi < 23.0:
                thong_bao = f"{bmi} · {phan_loai}; nên có {min_weight} – {max_weight} kg"
            else:
                thong_bao = f"{bmi} · {phan_loai}"

    return render_template(
        "index.html",
        cao=cao,
        nang=nang,
        thong_bao=thong_bao,
        mau_ket_qua=mau_ket_qua,
    )


if __name__ == "__main__":
    app.run(debug=True)