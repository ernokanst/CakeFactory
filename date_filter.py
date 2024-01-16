from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField
from wtforms.validators import DataRequired
from datetime import date


class DateFilterForm(FlaskForm):
    date_from = DateField('От', validators=[DataRequired()], default=date.today())
    date_till = DateField('До', validators=[DataRequired()])
    submit = SubmitField('Фильтр')