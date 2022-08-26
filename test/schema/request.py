from wtforms import Form
from wtforms.fields import FieldList, FloatField, FormField, IntegerField
from wtforms.validators import DataRequired


class UserSalaryRequest(Form):
    salary = FloatField('salary')


class UserRequest(Form):
    id = IntegerField('id', validators=[DataRequired()])
    ages = FieldList(IntegerField)
    salaries = FieldList(FormField(UserSalaryRequest))
