from datetime import timedelta
import os
import re

from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, make_response
)
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField
)
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo, Regexp, ValidationError
)
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "dev-key-thay-doi-khi-trien-khai"
)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)


# =====================================================
# TÀI KHOẢN
# =====================================================

# Tài khoản mẫu của Bài 4.
# Dùng mật khẩu băm thay vì lưu mật khẩu trực tiếp.
USERS = {
    "Phát": {
        "password": generate_password_hash("Phat123456"),
        "email": "phat@example.com",
    }
}


REMEMBER_COOKIE = "remember_login"
COOKIE_MAX_AGE = 30 * 24 * 60 * 60

remember_serializer = URLSafeTimedSerializer(
    app.config["SECRET_KEY"],
    salt="remember-login-v1"
)


# =====================================================
# BÀI 5: FORM ĐĂNG KÝ
# =====================================================

class RegisterForm(FlaskForm):
    username = StringField(
        "Tên đăng nhập",
        validators=[
            DataRequired(message="Vui lòng nhập tên đăng nhập."),
            Length(
                min=4,
                max=20,
                message="Tên đăng nhập phải dài từ 4 đến 20 ký tự."
            ),
            Regexp(
                r"^[a-z0-9_-]+$",
                message=(
                    "Tên đăng nhập chỉ được chứa chữ thường không dấu, "
                    "số, dấu gạch dưới (_) và dấu gạch ngang (-)."
                )
            )
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Vui lòng nhập email."),
            Email(message="Email không đúng định dạng.")
        ]
    )

    password = PasswordField(
        "Mật khẩu",
        validators=[
            DataRequired(message="Vui lòng nhập mật khẩu."),
            Length(
                min=8,
                message="Mật khẩu phải có ít nhất 8 ký tự."
            )
        ]
    )

    confirm_password = PasswordField(
        "Nhập lại mật khẩu",
        validators=[
            DataRequired(message="Vui lòng nhập lại mật khẩu."),
            EqualTo(
                "password",
                message="Mật khẩu nhập lại không khớp."
            )
        ]
    )

    agree = BooleanField("Tôi đồng ý với điều khoản sử dụng")

    submit = SubmitField("Đăng ký tài khoản")

    def validate_username(self, field):
        if field.data in USERS:
            raise ValidationError(
                "Tên đăng nhập đã được sử dụng."
            )

    def validate_email(self, field):
        email = field.data.strip().lower()

        for user in USERS.values():
            if user["email"].lower() == email:
                raise ValidationError(
                    "Email này đã được sử dụng."
                )

    def validate_agree(self, field):
        if not field.data:
            raise ValidationError(
                "Bạn phải đồng ý với điều khoản."
            )


# =====================================================
# KHÔI PHỤC ĐĂNG NHẬP
# =====================================================

@app.before_request
def restore_login():
    if session.get("user"):
        return

    token = request.cookies.get(REMEMBER_COOKIE)

    if not token:
        return

    try:
        username = remember_serializer.loads(
            token,
            max_age=COOKIE_MAX_AGE
        )
    except (BadSignature, SignatureExpired):
        return

    if username in USERS:
        session["user"] = username
        session.permanent = True


# =====================================================
# BÀI 1: MÁY TÍNH
# =====================================================

def chuyen_so(gia_tri):
    gia_tri = gia_tri.strip()

    if not gia_tri:
        raise ValueError("Vui lòng nhập một số.")

    if "," in gia_tri and "." in gia_tri:
        raise ValueError(
            "Vui lòng chỉ sử dụng dấu phẩy hoặc dấu chấm thập phân."
        )

    try:
        return float(gia_tri.replace(",", "."))
    except ValueError:
        raise ValueError("Vui lòng nhập một số hợp lệ.")


def dinh_dang_so(so):
    if so.is_integer():
        return str(int(so))

    return f"{so:.10g}"


# =====================================================
# BÀI 2: TÍNH ĐIỂM HỌC PHẦN
# =====================================================

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


# =====================================================
# BÀI 3: TÍNH BMI
# =====================================================

def kiem_tra_bmi(cao_str, nang_str):
    c_val = str(cao_str).strip() if cao_str is not None else ""
    n_val = str(nang_str).strip() if nang_str is not None else ""

    if not c_val and not n_val:
        return "Lỗi cả hai ô", None, None

    if not c_val:
        return "Lỗi ô chiều cao: Vui lòng nhập chiều cao.", None, None

    if not n_val:
        return "Lỗi ô cân nặng: Vui lòng nhập cân nặng.", None, None

    try:
        cao = float(c_val.replace(",", "."))
    except ValueError:
        return "Lỗi ô chiều cao: Vui lòng nhập một số.", None, None

    try:
        nang = float(n_val.replace(",", "."))
    except ValueError:
        return "Lỗi ô cân nặng: Vui lòng nhập một số.", None, None

    if cao < 50 or cao > 250:
        return (
            "Lỗi ô chiều cao: Giá trị phải từ 50 đến 250 cm.",
            None,
            None
        )

    if nang < 10 or nang > 300:
        return (
            "Lỗi ô cân nặng: Giá trị phải từ 10 đến 300 kg.",
            None,
            None
        )

    return None, cao, nang


# =====================================================
# BÀI 4: ĐĂNG NHẬP
# =====================================================

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user"):
        return redirect(url_for("index"))

    username = ""
    remember = False

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        remember = request.form.get("remember") == "on"

        if not username or not password:
            flash(
                "Vui lòng nhập tên đăng nhập và mật khẩu.",
                "error"
            )
            return render_template(
                "login.html",
                username=username,
                remember=remember
            )

        user = USERS.get(username)

        if user and check_password_hash(user["password"], password):
            session["user"] = username

            response = make_response(
                redirect(url_for("index"))
            )

            flash(
                f"Đăng nhập thành công. Xin chào {username}!",
                "success"
            )

            if remember:
                session.permanent = True

                token = remember_serializer.dumps(username)

                response.set_cookie(
                    REMEMBER_COOKIE,
                    token,
                    max_age=COOKIE_MAX_AGE,
                    httponly=True,
                    secure=False,
                    samesite="Lax",
                    path="/"
                )
            else:
                response.delete_cookie(
                    REMEMBER_COOKIE,
                    path="/"
                )

            return response

        flash(
            "Sai tên đăng nhập hoặc mật khẩu.",
            "error"
        )

    return render_template(
        "login.html",
        username=username,
        remember=remember
    )


# =====================================================
# BÀI 5: ĐĂNG KÝ
# =====================================================

@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user"):
        return redirect(url_for("index"))

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip().lower()
        password = form.password.data

        # Kiểm tra lại tên đăng nhập trước khi thêm tài khoản.
        # Cần thiết nếu sau này ứng dụng có nhiều người dùng đồng thời.
        if username in USERS:
            form.username.errors.append(
                "Tên đăng nhập đã được sử dụng."
            )
            return render_template(
                "register.html",
                form=form
            )

        USERS[username] = {
            "password": generate_password_hash(password),
            "email": email
        }

        flash(
            "Đăng ký thành công. Vui lòng đăng nhập.",
            "success"
        )

        return redirect(url_for("login"))

    return render_template(
        "register.html",
        form=form
    )


# =====================================================
# BÀI 4: ĐĂNG XUẤT
# =====================================================

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()

    response = make_response(
        redirect(url_for("login"))
    )

    response.delete_cookie(
        REMEMBER_COOKIE,
        path="/"
    )

    flash("Bạn đã đăng xuất.", "success")

    return response


# =====================================================
# HỒ SƠ CÁ NHÂN
# =====================================================

@app.route("/profile")
def profile():
    if not session.get("user"):
        flash("Vui lòng đăng nhập.", "error")
        return redirect(url_for("login"))

    return render_template(
        "profile.html",
        username=session["user"]
    )


# =====================================================
# TRANG CHÍNH: BÀI 1, 2, 3
# =====================================================

@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("user"):
        flash("Vui lòng đăng nhập.", "error")
        return redirect(url_for("login"))

    bai = request.values.get("bai", "1")

    if bai not in {"1", "2", "3"}:
        bai = "1"

    a, b, op = "", "", "+"
    loi_a, loi_b, loi_op = "", "", ""
    ket_qua_1 = ""

    cc, gk, ck = "", "", ""
    thong_bao_2 = ""

    cao, nang = "", ""
    thong_bao_3 = ""
    mau_3 = "success"

    if request.method == "POST":

        # ---------------- BÀI 1 ----------------
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
                    ket_qua_1 = (
                        f"{dinh_dang_so(so_a)} {op} "
                        f"{dinh_dang_so(so_b)} = "
                        f"{dinh_dang_so(kq)}"
                    )

        # ---------------- BÀI 2 ----------------
        elif bai == "2":
            cc = request.form.get("cc", "")
            gk = request.form.get("gk", "")
            ck = request.form.get("ck", "")

            res_cc = kiem_tra_diem(cc, "CC")
            res_gk = kiem_tra_diem(gk, "GK")
            res_ck = kiem_tra_diem(ck, "CK")

            loi = [
                x for x in (res_cc, res_gk, res_ck)
                if isinstance(x, str)
            ]

            if res_cc == res_gk == res_ck == "Trống":
                thong_bao_2 = "Lỗi cả 3 ô."

            elif loi:
                thong_bao_2 = loi[0]

            else:
                diem_hp = round(
                    res_cc * 0.1 +
                    res_gk * 0.3 +
                    res_ck * 0.6,
                    1
                )

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

        # ---------------- BÀI 3 ----------------
        elif bai == "3":
            cao = request.form.get("cao", "")
            nang = request.form.get("nang", "")

            err, val_cao, val_nang = kiem_tra_bmi(
                cao, nang
            )

            if err:
                thong_bao_3 = err
                mau_3 = "error-box"

            else:
                cao_m = val_cao / 100
                bmi = round(
                    val_nang / (cao_m ** 2),
                    1
                )

                min_weight = round(
                    18.5 * cao_m ** 2,
                    1
                )

                max_weight = round(
                    22.9 * cao_m ** 2,
                    1
                )

                if bmi < 18.5:
                    phan_loai = "Thiếu cân"
                    mau_3 = "warning"

                elif bmi < 23:
                    phan_loai = "Bình thường"
                    mau_3 = "success"

                elif bmi < 25:
                    phan_loai = "Thừa cân"
                    mau_3 = "warning"

                else:
                    phan_loai = "Béo phì"
                    mau_3 = "danger"

                if 18.5 <= bmi < 23:
                    thong_bao_3 = (
                        f"BMI: {bmi} · {phan_loai}. "
                        f"Khoảng cân nặng tham khảo: "
                        f"{min_weight} – {max_weight} kg."
                    )
                else:
                    thong_bao_3 = (
                        f"BMI: {bmi} · {phan_loai}."
                    )

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
        username=session.get("user", "")
    )


if __name__ == "__main__":
    app.run(debug=True)