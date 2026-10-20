from flask import Flask, render_template
app = Flask(__name__)
students = [
 {"id":"SV001","name":"Trần Minh An","score":8.5},
 {"id":"SV002","name":"Lê Thu Hà","score":6.8},
 {"id":"SV003","name":"Phạm Quốc Bảo","score":4.5},
 {"id":"SV004","name":"Nguyễn Ngọc Mai","score":9.2},
 {"id":"SV005","name":"Đỗ Hoàng Nam","score":5.0},
]
@app.route("/")
def home():
    return render_template("grades.html", students=students)
if __name__ == "__main__": app.run(debug=True)
