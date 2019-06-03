from flask import Flask, render_template, request, Response, redirect, url_for
import json
import searchform
import similarity
import scraping
from flask_wtf import FlaskForm
from wtforms import TextField, Form, StringField
from wtforms.validators import DataRequired


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

messages = [["machine-message" ,"Welcome to ChatFAQs! Please ask your question using the text box at the bottom of the screen."]]
messages2 = [["machine-message" ,"Welcome to ChatFAQs! Please ask your question using the text box at the bottom of the screen."],
            ["user-message", "How do I log in?"]]

def fixqs(questions):
    return "".join([str(x) for x in questions.contents])


formatted_qs = [fixqs(q) for q in questions]


class SearchForm(Form):
    autocomp = TextField('Please type your question', id='question_autocomplete')


class MessageForm(FlaskForm):
    message = StringField('Message', id='user_message', validators=[DataRequired()])



@app.route("/search", methods=["GET", "POST"])
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

@app.route("/testing", methods=['GET'])
def dropdown():
    colors = ['Red', 'Blue', 'Black', 'Orange']
    return render_template("testing.html", colors = colors)
"""
@app.route("/testing2", methods=['GET','POST'])
def testing2():
    form = MessageForm(request.form)
    # print(f'starting')
    if form.validate_on_submit():
    #     messages.append(["user-message", form.message.data])
    #     print(f'------1-------')
    #     print(f'{form.message.data}')
    #     return render_template("testing2.html", form=form, messages=messages, placeholder="Begin writing your message here")

        return redirect(url_for('send_message'))
    return render_template("testing2.html", form=form, messages=messages,  placeholder="Begin writing your message here")

@app.route("/send_message", methods=['GET','POST'])
def send_message():
    form = MessageForm(request.form)
    print(f'starting')
    if form.validate_on_submit():
        messages.append(["user-message", form.message.data])
        print(f'------1-------')
        print(f'{form.message.data}')
        return render_template("testing2.html", form=form, messages=messages, placeholder="Begin writing your message here")
    # return render_template("testing2.html", form=form, messages=messages,  placeholder="Begin writing your message here")
    return redirect(url_for('testing2'))
"""

#--THIS MIGHT NOT WORK:--
@app.route("/testing3", methods=['GET', 'POST'])
def initialize():
    message_form = MessageForm(request.form)
    if message_form.validate_on_submit:
        return redirect(url_for('sending_message')) 
    return render_template("testing2.html", form=message_form, messages=messages, placeholder="Begin writing your message here")

@app.route("/sending_message", methods=['GET', 'POST'])
def sending_message():
    message_form = MessageForm(request.form)
    if message_form.validate_on_submit():
        # add user message
        messages.append(["user-message", message_form.message.data])

        # handle matching
        messages.append(["machine-message", "This is the Machine's response to your message."])

        return redirect(url_for('initialize'))
    return render_template("testing2.html", form=message_form, messages=messages, placehold="Begin writing your message here")


if __name__ == "__main__":
    app.run(debug=True)
