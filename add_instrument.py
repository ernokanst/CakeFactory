from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired


class AddInstrumentForm(FlaskForm):
    naimenovanie = StringField('Наименование', validators=[DataRequired()])
    opisanie = StringField('Описание')
    tip_instrumenta = StringField('Тип инструмента', validators=[DataRequired()])
    stepen_iznosa = StringField('Степень износа')
    postavschik = StringField('Поставщик')
    data_priobreteniya = DateField('Дата приобретения', validators=[DataRequired()])
    kolichestvo = IntegerField('Количество', validators=[DataRequired()])
    submit = SubmitField('Добавить')