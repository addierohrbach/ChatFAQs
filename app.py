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



questions = scraping.questions
indexanchor = 0
messages = [["machine-message1" ,"Welcome to ChatFAQs! Please ask your question using the text box at the bottom of the screen.", 0]]
messages2 = [["machine-message" ,"Welcome to ChatFAQs! Please ask your question using the text box at the bottom of the screen."],
            ["user-message", "How do I log in?"]]

def fixqs(questions):
    return "".join([str(x) for x in questions.contents])


formatted_qs = [fixqs(q) for q in questions]



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


def click_alt_question():
    # global indexanchor
    # indexanchor = len(messages)
    # messages.append(["user-message", question[1], len(messages)])
    # similar_qs = None
    # # handle matching
    # if len(messages)> 3:
    #     index = None
    #     for message in reversed(messages):
    #         if message[0] == 'machine-message':
    #             #print(message)
    #             index = message[1][3]
    #             break                
    #     similar_qs = similarity.predictusinganswer(index, message_form.message.data)
    # else:
    #     similar_qs = similarity.predict(message_form.message.data)
    # messages.append(["machine-message", question, len(messages)])
    # if len(similar_qs)> 1:
    #     messages.append(["machine-message1" ,"If this does not answer your question here are some other possibilites. You can also ask another question by typing it into the text box at the bottom of the screen."])
    #     for i in range(1,4):
    #         if i >= len(similar_qs): break
    #         messages.append(["alt-questions", similar_qs[i], len(messages)])

    return redirect(url_for('initialize', _anchor='anchor'))
    # make value = message[2] in testing2?
    # look up messages[that index] in python. found message = message
    #  find index of that by message[1][3]
    # similarity.returnquestion(index)
    #return render_template("testing2.html", onclick=click_alt_question, form=message_form, messages=messages, indexanchor = indexanchor, placeholder="Begin writing your message here")

#--THIS MIGHT NOT WORK:--
@app.route("/testing3", methods=['GET', 'POST'])
def initialize():
    message_form = MessageForm(request.form)
    if message_form.validate_on_submit:
        return redirect(url_for('sending_message')) 
    return render_template("testing2.html", onclickfun=click_alt_question, form=message_form, messages=messages, indexanchor = indexanchor, placeholder="Begin writing your message here")


@app.route("/sending_message", methods=['GET', 'POST'])
def sending_message():
    message_form = MessageForm(request.form)
    global indexanchor
    #not sure where this goes but for button
    #     
    if message_form.validate_on_submit():
        indexanchor = len(messages)
        # add user message
        messages.append(["user-message", message_form.message.data, len(messages)])
        similar_qs = None
        # handle matching
        if len(messages)> 3:
            index = None
            for message in reversed(messages):
                if message[0] == 'machine-message':
                    #print(message)
                    if len(message[1])>3:
                        index = message[1][3]
                    else: index = None
                    break                
            if index == None:
                similar_qs = similarity.predict(message_form.message.data)
            else: similar_qs = similarity.predictusinganswer(index, message_form.message.data)
        else:
            similar_qs = similarity.predict(message_form.message.data)
        messages.append(["machine-message", similar_qs[0], len(messages)])
        if len(similar_qs)> 1:
            messages.append(["machine-message1" ,"If this does not answer your question here are some other possibilites. You can also ask another question by typing it into the text box at the bottom of the screen."])
            for i in range(1,4):
                if i >= len(similar_qs): break
                messages.append(["alt-questions", similar_qs[i], len(messages)])

        return redirect(url_for('initialize', _anchor='anchor'))
    return render_template("testing2.html", form=message_form, messages=messages, indexanchor = indexanchor, placehold="Begin writing your message here", onclickfun=click_alt_question)


if __name__ == "__main__":
    app.run(debug=True)
