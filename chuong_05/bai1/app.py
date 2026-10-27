
from flask import Flask, render_template, request

app = Flask(__name__)


def chuyen_so(gia_tri):
    """Chuyển chuỗi thành số, chấp nhận dấu phẩy hoặc dấu chấm."""
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
    """Bỏ phần thập phân .0 nếu kết quả là số nguyên."""
    if so.is_integer():
        return str(int(so))
    return f"{so:.10g}"


@app.route("/", methods=["GET", "POST"])
def index():
    a = ""
    b = ""
    op = "+"
    loi_a = ""
    loi_b = ""
    loi_op = ""
    ket_qua = ""

    if request.method == "POST":
        a = request.form.get("a", "")
        b = request.form.get("b", "")
        op = request.form.get("op", "+")

        # Kiểm tra phép toán trước khi tính
        if op not in ["+", "-", "*", "/"]:
            loi_op = "Phép toán không hợp lệ."

        # Kiểm tra số thứ nhất
        try:
            so_a = chuyen_so(a)
        except ValueError as e:
            loi_a = str(e)
            so_a = None

        # Kiểm tra số thứ hai
        try:
            so_b = chuyen_so(b)
        except ValueError as e:
            loi_b = str(e)
            so_b = None

        # Chỉ tính khi cả hai số và phép toán đều hợp lệ
        if not loi_a and not loi_b and not loi_op:
            if op == "+":
                kq = so_a + so_b

            elif op == "-":
                kq = so_a - so_b

            elif op == "*":
                kq = so_a * so_b

            else:  # op == "/"
                if so_b == 0:
                    loi_b = "Không thể chia cho 0."
                    kq = None
                else:
                    kq = so_a / so_b

            if kq is not None:
                ket_qua = (
                    f"{dinh_dang_so(so_a)} {op} "
                    f"{dinh_dang_so(so_b)} = {dinh_dang_so(kq)}"
                )

    return render_template(
        "index.html",
        a=a,
        b=b,
        op=op,
        loi_a=loi_a,
        loi_b=loi_b,
        loi_op=loi_op,
        ket_qua=ket_qua
    )


if __name__ == "__main__":
    app.run(debug=True)
