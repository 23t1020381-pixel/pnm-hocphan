from flask import Flask, render_template
app = Flask(__name__)
@app.context_processor
def common(): return {"site_name":"Hồ sơ của Phát"}
@app.route("/")
def home(): return render_template("home.html", title="Trang chủ")
@app.route("/hoc-van")
def education(): return render_template("education.html", title="Học vấn")
@app.route("/du-an")
def projects(): return render_template("projects.html", title="Dự án")
@app.route("/lien-he")
def contact(): return render_template("contact.html", title="Liên hệ")
if __name__ == "__main__": app.run(debug=True)
