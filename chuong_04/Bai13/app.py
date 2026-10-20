from flask import Flask, render_template, abort
app=Flask(__name__)
posts={1:{"title":"Bài viết đầu tiên","content":"Nội dung bài viết số một."},2:{"title":"Bài viết thứ hai","content":"Nội dung bài viết số hai."}}
@app.route("/")
def home(): return render_template("posts.html",posts=posts)
@app.route("/post/<int:post_id>")
def post_detail(post_id):
    post=posts.get(post_id)
    if post is None: abort(404,description=f"Không tìm thấy bài viết {post_id}")
    return render_template("post_detail.html",post=post)
@app.errorhandler(404)
def not_found(error): return render_template("404.html",message=error.description),404
if __name__=="__main__": app.run(debug=True)
