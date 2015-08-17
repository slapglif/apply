from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired


class xForm(Form):
    ign = StringField('ign')
    community = StringField('community')
    email = StringField('email')
    age = StringField('name')
    search = StringField('search')

    dd1 = SelectField('Rank', choices=[])
    submit = SubmitField('Submit Application!')


def __init__(self):
    Form.__init__(self)