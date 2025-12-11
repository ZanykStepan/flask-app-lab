from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Ім’я користувача', validators=[
        DataRequired(message="Це поле обов'язкове")
    ])

    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=4, max=10, message="Пароль має бути від 4 до 10 символів")
    ])

    remember = BooleanField("Запам'ятати мене")

    submit = SubmitField('Увійти')


class RegistrationForm(FlaskForm):
    username = StringField('Ім’я користувача', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Повторіть пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зареєструватися')
