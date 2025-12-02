from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp


class ContactForm(FlaskForm):
    name = StringField('Ім’я', validators=[
        DataRequired(message="Це поле обов'язкове"),
        Length(min=4, max=10, message="Довжина має бути від 4 до 10 символів")
    ])

    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Некоректний email")
    ])

    phone = StringField('Телефон', validators=[
        DataRequired(),
        Regexp(r'^\+380\d{9}$', message="Формат: +380XXXXXXXXX")
    ])

    subject = SelectField('Тема', choices=[
        ('consultation', 'Консультація'),
        ('order', 'Замовлення'),
        ('collaboration', 'Співпраця'),
        ('other', 'Інше')
    ])

    message = TextAreaField('Повідомлення', validators=[
        DataRequired(),
        Length(max=500, message="Не більше 500 символів")
    ])

    submit = SubmitField('Надіслати')
