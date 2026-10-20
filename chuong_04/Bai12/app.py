from flask import Flask, render_template
app=Flask(__name__)
@app.route("/")
def home(): return render_template("page.html",title="Trang chủ",active="home",message="Chào mừng bạn.")
@app.route("/gioi-thieu")
def about(): return render_template("page.html",title="Giới thiệu",active="about",message="Thông tin giới thiệu.")
@app.route("/lien-he")
def contact(): return render_template("page.html",title="Liên hệ",active="contact",message="Thông tin liên hệ.")
if __name__=="__main__": app.run(debug=True)
