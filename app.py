from flask import Flask, render_template, request, Response
import json
import searchform
import similarity
import scraping
from wtforms import TextField, Form


app = Flask(__name__)
app.secret_key = 'aoijad.asdofij230f-ds'

cities = ["Bratislava",
          "Banská Bystrica",
          "Prešov",
          "Považská Bystrica",
          "Žilina",
          "Košice",
          "Ružomberok",
          "Zvolen",
          "Poprad"]

questions = scraping.questions


def fixqs(questions):
    return "".join([str(x) for x in questions.contents])


formatted_qs = [fixqs(q) for q in questions]


class SearchForm(Form):
    autocomp = TextField('Please type your question', id='question_autocomplete')


@app.route("/search", methods=("GET", "POST"))
def view_answer_similarity():
    form = searchform.SearchForm()
    if form.validate_on_submit():
        print(f'-------------User Input:-------------')
        print(form.question.data)
        similar_qs = similarity.predict(form.question.data)
        return render_template("layout2.html", form=form, similar_qs=similar_qs)
    return render_template("layout2.html", form=form, answer="", matched_q="")


@app.route("/", methods=['GET', 'POST'])
def index():
    form = SearchForm(request.form)
    return render_template("search.html", form=form)


@app.route("/_autocomplete", methods=['GET'])
def autocomp():
    return Response(json.dumps(formatted_qs), mimetype='application/json')


if __name__ == "__main__":
    app.run(debug=True)
