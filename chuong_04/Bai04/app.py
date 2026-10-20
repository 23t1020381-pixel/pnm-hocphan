from flask import Flask, render_template
app = Flask(__name__)
examples = [
 ("{{ 'flask'|title }}", "Flask"),
 ("{{ '  hello  '|trim }}", "hello"),
 ("{{ [1,2,3]|length }}", "3"),
 ("{{ 'abc'|upper }}", "ABC"),
 ("{{ 1500000|int }}", "1500000"),
 ("{{ 'a,b,c'|replace(',', '-') }}", "a-b-c"),
 ("{{ 'python'|capitalize }}", "Python"),
 ("{{ [3,1,2]|sort|join(', ') }}", "1, 2, 3"),
]
@app.route("/")
def home(): return render_template("filters.html", examples=examples)
if __name__ == "__main__": app.run(debug=True)
