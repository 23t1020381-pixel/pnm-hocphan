from flask import Flask, render_template, redirect, url_for
app=Flask(__name__)
products=[{"id":1,"name":"Bàn phím cơ","price":850000,"category":"Phụ kiện"},{"id":2,"name":"Chuột không dây","price":320000,"category":"Phụ kiện"},{"id":3,"name":"Tai nghe","price":590000,"category":"Âm thanh"},{"id":4,"name":"Webcam HD","price":450000,"category":"Phụ kiện"},{"id":5,"name":"Loa mini","price":390000,"category":"Âm thanh"},{"id":6,"name":"USB 64GB","price":180000,"category":"Lưu trữ"},{"id":7,"name":"Ổ cứng SSD","price":1250000,"category":"Lưu trữ"},{"id":8,"name":"Đế laptop","price":260000,"category":"Phụ kiện"}]
cart=[]
@app.route("/")
def home(): return render_template("products.html",products=products,cart_count=len(cart))
@app.route("/add/<int:product_id>", methods=["POST"])
def add(product_id):
    if any(p["id"]==product_id for p in products): cart.append(product_id)
    return redirect(url_for("home"))
if __name__=="__main__": app.run(debug=True)
