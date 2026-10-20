from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
comments = [{"name":"Lan","content":"Bài viết rất hữu ích."}]
@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name","Ẩn danh").strip()[:60] or "Ẩn danh"
        content = request.form.get("content","").strip()[:500]
        if content: comments.append({"name":name,"content":content})
        return redirect(url_for("home"))
    return render_template("comments.html", comments=comments)
if __name__ == "__main__": app.run(debug=True)
