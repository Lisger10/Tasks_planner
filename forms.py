from wtforms import Form, StringField, validators, DateField, RadioField, ValidationError
import datetime
from wtforms.widgets import TextArea


CHOICES = [('Обычный', 'Обычный'), ('Срочный', 'Срочный')]

class CreateTaskForm(Form):
    task = StringField('Название', [validators.Length(min=1, max = 80)])
    date = DateField('Дата создания', default = datetime.date)
    priority = RadioField('Приоритет', choices=CHOICES, default='Обычный' )

