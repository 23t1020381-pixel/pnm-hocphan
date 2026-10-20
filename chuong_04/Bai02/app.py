from flask import Flask, render_template
app = Flask(__name__)
@app.route("/")
def home():
    # Đường dẫn đúng: templates/profile.html
    return render_template("profile.html", name="Nguyễn Đăng Phát")
if __name__ == "__main__":
    app.run(debug=True)
