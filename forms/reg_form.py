from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    age = IntegerField('Возраст')
    position = TextAreaField('Должность', validators=[DataRequired()])
    speciality = TextAreaField('Сециальность', validators=[DataRequired()])
    address = TextAreaField('Адресс', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
