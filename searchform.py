from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class SearchForm(Form):
    question = StringField(
        'question',
        validators=[DataRequired()]
    )