from datetime import timedelta
import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    make_response,
)
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

app = Flask(__name__)

# Khóa bí mật dùng cho session và cookie.
# Khi triển khai thực tế, hãy đặt SECRET_KEY bằng biến môi trường.
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "dev-key-thay-doi-khi-trien-khai"
)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)

REMEMBER_COOKIE = "remember_login"
COOKIE_MAX_AGE = 30 * 24 * 60 * 60

# Tài khoản mẫu theo đề bài.
USERS = {
    "admin": "admin123",
    "Phát": "Phat123456",
}

remember_serializer = URLSafeTimedSerializer(
    app.config["SECRET_KEY"],
    salt="remember-login-v1",
)


@app.before_request
def restore_login():
    """Khôi phục session từ cookie nếu người dùng đã chọn Ghi nhớ."""
    if session.get("user"):
        return

    token = request.cookies.get(REMEMBER_COOKIE)
    if not token:
        return

    try:
        username = remember_serializer.loads(
            token,
            max_age=COOKIE_MAX_AGE,
        )
    except (BadSignature, SignatureExpired):
        return

    if username in USERS:
        session["user"] = username
        session.permanent = True


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Người đã đăng nhập không cần đăng nhập lại.
    if session.get("user"):
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        remember = request.form.get("remember") == "on"

        if not username or not password:
            flash("Vui lòng nhập tên đăng nhập và mật khẩu.", "error")
            return render_template(
                "login.html",
                username=username,
                remember=remember,
            )

        # So sánh chính xác, có phân biệt chữ hoa và chữ thường.
        if username in USERS and USERS[username] == password:
            session["user"] = username

            response = make_response(redirect(url_for("index")))
            flash(f"Đăng nhập thành công. Xin chào {username}!", "success")

            if remember:
                session.permanent = True
                token = remember_serializer.dumps(username)
                response.set_cookie(
                    REMEMBER_COOKIE,
                    token,
                    max_age=COOKIE_MAX_AGE,
                    httponly=True,
                    secure=False,  # Dùng False khi chạy localhost bằng HTTP.
                    samesite="Lax",
                    path="/",
                )
            else:
                response.delete_cookie(REMEMBER_COOKIE, path="/")

            return response

        flash("Sai tên đăng nhập hoặc mật khẩu.", "error")
        return render_template(
            "login.html",
            username=username,
            remember=remember,
        )

    return render_template("login.html", username="", remember=False)


@app.route("/profile")
def profile():
    if not session.get("user"):
        flash("Vui lòng đăng nhập.", "error")
        return redirect(url_for("login"))

    return render_template("profile.html", username=session["user"])


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()

    response = make_response(redirect(url_for("index")))
    response.delete_cookie(REMEMBER_COOKIE, path="/")

    flash("Bạn đã đăng xuất.", "success")
    return response


if __name__ == "__main__":
    app.run(debug=True)