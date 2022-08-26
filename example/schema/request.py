from wtforms import Form
from wtforms.fields import IntegerField


class UserForm(Form):
    user_id = IntegerField()
