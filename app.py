from flask import Flask, render_template, url_for, redirect
from flask_wtf.csrf import CSRFProtect

import searchform
import matching


app = Flask(__name__)
app.secret_key = 'aoijad.asdofij230f-ds'


@app.route("/", methods=("GET", "POST"))
def view_answer():
    form = searchform.SearchForm()
    if form.validate_on_submit():
        print(form.question.data)
        answer = matching.predict(form.question.data)
        print(answer)
        return render_template("question.html", form=form, answer=answer)
    return render_template("question.html", form=form, answer="answer")


if __name__ == "__main__":
    app.run(debug=True)