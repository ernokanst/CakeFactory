from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField, DecimalField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired


class DecorationForm(FlaskForm):
    artikul = IntegerField('Артикул')
    naimenovanie = StringField('Наименование', validators=[DataRequired()])
    edinitsa_izmereniya = StringField('Единица измерения', validators=[DataRequired()])
    kolichestvo = DecimalField('Количество', validators=[DataRequired()])
    postavschik = StringField('Поставщик')
    izobrazhenie = FileField('Изображение', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    tip_ukrasheniya = StringField('Тип украшения', validators=[DataRequired()])
    zakupochnaya_tsena = DecimalField('Закупочная цена', validators=[DataRequired()])
    ves = StringField('Вес', validators=[DataRequired()])
    srok_godnosti = DateField('Срок годности')
    submit = SubmitField('Обновить')