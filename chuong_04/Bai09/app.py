from flask import Flask, render_template, request, url_for
app=Flask(__name__)
posts=[{"id":i,"title":f"Bài viết số {i}"} for i in range(1,36)]
@app.route("/")
def home():
    page=max(1, request.args.get("page",1,type=int))
    per_page=5
    total_pages=(len(posts)+per_page-1)//per_page
    page=min(page,total_pages)
    data=posts[(page-1)*per_page:page*per_page]
    return render_template("posts.html", posts=data, page=page, total_pages=total_pages, endpoint="home")
if __name__=="__main__": app.run(debug=True)
