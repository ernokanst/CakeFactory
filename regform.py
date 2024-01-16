from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename


def password_check(form, field):
    l = field.data and len(field.data) or 0
    if l < 5 or 20 != -1 and l > 20:
        raise ValidationError('Пароль должен содержать от 5 до 20 символов')
    has_upper = False
    for s in field.data:
        if s.isupper():
            has_upper = True
            break
    if not has_upper:
        raise ValidationError('В пароле должны встречаться заглавные буквы')
    has_lower = False
    for s in field.data:
        if s.islower():
            has_lower = True
            break
    if not has_lower:
        raise ValidationError('В пароле должны встречаться маленькие буквы')        


class RegForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), password_check])
    repassword = PasswordField(
        'Повторите пароль', validators=[DataRequired()])
    fio = StringField('ФИО')
    content = FileField('Аватар', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Зарегистрироваться')
