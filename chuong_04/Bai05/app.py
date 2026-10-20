from datetime import datetime
from flask import Flask, render_template
app = Flask(__name__)
@app.template_filter("vnd")
def vnd(value):
    return f"{int(value):,}".replace(",", ".") + " đ"
@app.template_filter("date_vi")
def date_vi(value):
    if isinstance(value, str): value = datetime.fromisoformat(value)
    return value.strftime("%d/%m/%Y")
@app.template_filter("short_text")
def short_text(value, length=40):
    value = str(value)
    return value if len(value) <= length else value[:length-1] + "…"
items = [
 {"name":"Bàn phím cơ","price":850000,"date":"2026-03-12","description":"Bàn phím cơ nhỏ gọn dùng cho học tập và làm việc."},
 {"name":"Chuột không dây","price":320000,"date":"2026-05-20","description":"Chuột không dây có thời lượng pin lâu và thiết kế tiện dụng."}
]
@app.route("/")
def home(): return render_template("filters.html", items=items)
if __name__ == "__main__": app.run(debug=True)
