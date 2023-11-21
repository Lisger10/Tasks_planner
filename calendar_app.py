from flask import Flask, request, redirect
from flask import json
from flask import render_template
from wtforms import Form, SubmitField, StringField, validators
from forms import CreateTaskForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Date, Integer, Boolean
from datetime import date
from flask import flash
import plotly.graph_objects as go
from plotly.offline import plot
from flask import url_for




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db = SQLAlchemy()
db.init_app(app)


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True )
    task = db.Column(db.String(80), nullable = False )
    date = db.Column(db.Date)
    priority = db.Column(db.String(7))
    status = db.Column(db.String, default = 'toDo')

    def __init__(self, task = 'None', date = 'None', priority = 'Обычный', status = 'toDo' ):
        self.task = task
        self.date = date
        self.priority = priority
        self.status = status



with app.app_context():
    db.create_all()


def tasks_status():
    tasks_toDo = Task.query.filter(Task.status =='toDo')
    tasks_done = Task.query.filter(Task.status == 'done')
    return tasks_toDo, tasks_done

def tasks_amount():
    tasks_toDo_count = Task.query.filter(Task.status =='toDo').count()
    tasks_done_count = Task.query.filter(Task.status == 'done').count()
    return tasks_toDo_count, tasks_done_count

@app.route('/', methods = ['GET', 'POST'])
def main_page():
    form = CreateTaskForm(request.form)
    if request.method == 'POST' and form.validate():
        today = date.today()
        task = Task(task = form.task.data, date=today, priority=form.priority.data, status = 'toDo' )
        db.session.add(task)
        db.session.commit()
        tasks_toDo, tasks_done = tasks_status()
        tasks_toDo_count, tasks_done_count = tasks_amount()
        fig = addGraph(tasks_toDo_count,tasks_done_count)
        return render_template('main.html', form = form, task= task, fig=fig, tasks_toDo = tasks_toDo, tasks_done=tasks_done,
                                 tasks_toDo_count= tasks_toDo_count,
                                 tasks_done_count= tasks_done_count )

    else:
        tasks_toDo, tasks_done = tasks_status()
        tasks_toDo_count, tasks_done_count = tasks_amount()
        fig = addGraph(tasks_toDo_count,tasks_done_count)
        return render_template('main.html', form=form, fig=fig, tasks_toDo = tasks_toDo, tasks_done=tasks_done, 
                                 tasks_toDo_count= tasks_toDo_count,
                                 tasks_done_count= tasks_done_count)


@app.route('/delete/<int:id>')
def delete(id):
   task = db.get_or_404(Task, id)
   db.session.delete(task)
   db.session.commit()
   return redirect(url_for('main_page'))

@app.route('/edit/<int:id>')
def edit(id):
    task = db.get_or_404(Task, id)
    task.status = 'done'
    db.session.commit()
    return redirect(url_for('main_page'))

def addGraph(value1, value2):
    labels = ['В работе','Выполнено']
    values = [value1, value2]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig= plot(fig, output_type="div")
    return fig

 

if __name__ == '__main__':
    app.run(debug= True)