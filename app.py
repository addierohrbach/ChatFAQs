from flask import Flask, render_template

import searchform
import similarity


app = Flask(__name__)
app.secret_key = 'aoijad.asdofij230f-ds'


@app.route("/", methods=("GET", "POST"))
def view_answer_similarity():
    form = searchform.SearchForm()
    if form.validate_on_submit():
        print(f'-------------User Input:-------------')
        print(form.question.data)
        similar_qs = similarity.predict(form.question.data)
        return render_template("layout2.html", form=form, similar_qs=similar_qs)
    return render_template("layout2.html", form=form, answer="", matched_q="")


if __name__ == "__main__":
    app.run(debug=True)
