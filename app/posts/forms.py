from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, DateTimeLocalField, SubmitField
from wtforms.validators import DataRequired, Length
from datetime import datetime

class PostForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired(), Length(min=2, max=150)])
    content = TextAreaField("Зміст", validators=[DataRequired()], render_kw={"rows": 5})
    category = SelectField("Категорія", choices=[('news', 'Новини'), ('tech', 'Технології'), ('life', 'Життя')], validators=[DataRequired()])
    publish_date = DateTimeLocalField("Дата публікації", format='%Y-%m-%dT%H:%M', default=datetime.now)
    is_active = BooleanField("Активний пост", default=True)
    submit = SubmitField("Зберегти")