from flask import Flask, render_template, url_for, redirect
from flask_wtf.csrf import CSRFProtect

import searchform
import matching
import similarity


app = Flask(__name__)
app.secret_key = 'aoijad.asdofij230f-ds'


@app.route("/", methods=("GET", "POST"))
def view_answer():
    form = searchform.SearchForm()
    if form.validate_on_submit():
        print(f'-------------User Input:-------------')
        print(form.question.data)
        matched_q, answer = matching.predict(form.question.data)
        print(f'-------------Matched Question:-------------')
        print(matched_q)
        print(f'-------------Matched Answer:-------------')
        print(answer)
        print(f'-------------End of Matched Answer:-------------')
        return render_template("layout.html", form=form, answer=answer, matched_q=matched_q)
    return render_template("layout.html", form=form, answer="", matched_q="")

@app.route("/similarity", methods=("GET", "POST"))
def view_answer_similarity():
    form = searchform.SearchForm()
    if form.validate_on_submit():
        print(f'-------------User Input:-------------')
        print(form.question.data)
        similar_qs = similarity.predict(form.question.data)
        return render_template("layout2.html", form=form, similar_qs=similar_qs)
    return render_template("layout.html", form=form, answer="", matched_q="")


if __name__ == "__main__":
    app.run(debug=True)
