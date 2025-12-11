from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class ResumeForm(FlaskForm):
    title = StringField('Бажана посада', validators=[DataRequired(), Length(min=2, max=100)])
    skills = StringField('Ключові навички', validators=[Length(max=200)])
    category = SelectField('Категорія', coerce=int, validators=[DataRequired()])
    description = TextAreaField('Про себе (досвід)', validators=[DataRequired()])
    submit = SubmitField('Зберегти')
