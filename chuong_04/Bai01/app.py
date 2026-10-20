from flask import Flask, render_template
app = Flask(__name__)
@app.route("/")
def home():
    profile = {"name":"Nguyễn Đăng Phát", "year":2026, "major":"Công nghệ thông tin",
               "skills":["Python","HTML","Jinja2"]}
    return render_template("profile.html", profile=profile)
if __name__ == "__main__":
    app.run(debug=True)
