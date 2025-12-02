from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


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