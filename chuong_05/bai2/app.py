from flask import Flask, render_template, request

app = Flask(__name__)


def kiem_tra_diem(value, ten_o):
    val = str(value).strip() if value is not None else ""
    if val == "":
        return "Trống"

    # Hỗ trợ cả dấu phẩy (,) và dấu chấm (.)
    val = val.replace(",", ".")

    try:
        num = float(val)
    except ValueError:
        return f"Lỗi ô {ten_o}: Vui lòng nhập một số."

    if num < 0 or num > 10:
        return f"Lỗi ô {ten_o}: Điểm phải từ 0 đến 10."

    return num


@app.route("/", methods=["GET", "POST"])
def index():
    thong_bao = ""
    cc_val, gk_val, ck_val = "", "", ""

    if request.method == "POST":
        cc_val = request.form.get("cc", "")
        gk_val = request.form.get("gk", "")
        ck_val = request.form.get("ck", "")

        res_cc = kiem_tra_diem(cc_val, "CC")
        res_gk = kiem_tra_diem(gk_val, "GK")
        res_ck = kiem_tra_diem(ck_val, "CK")

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
            thong_bao = "Lỗi cả 3 ô"
        elif len(loi) > 0:
            thong_bao = loi[0]
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

            thong_bao = f"{diem_hp} · {diem_chu}"

    return render_template(
        "index.html", thong_bao=thong_bao, cc=cc_val, gk=gk_val, ck=ck_val
    )


if __name__ == "__main__":
    app.run(debug=True)