from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo_list.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    todos = db.relationship('Todo', backref='user', lazy=True)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(150), nullable=False)
    reminder = db.Column(db.String(150))
    due_date = db.Column(db.Date)
    due_time = db.Column(db.Time)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registered successfully! Please log in.")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('todo_list'))
        flash("Invalid credentials! Please try again.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/todo', methods=['GET', 'POST'])
def todo_list():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        task = request.form['task']
        reminder = request.form['reminder']
        due_date = request.form.get('due_date', None)
        due_time = request.form.get('due_time', None)
        due_date = datetime.strptime(due_date, '%Y-%m-%d').date() if due_date else None
        due_time = datetime.strptime(due_time, '%H:%M').time() if due_time else None
        user_id = session['user_id']
        new_todo = Todo(task=task, reminder=reminder, due_date=due_date, due_time=due_time, user_id=user_id)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('todo_list'))
    
    todos = Todo.query.filter_by(user_id=session['user_id']).all()
    return render_template('todo.html', todos=todos)

@app.route('/delete/<int:id>')
def delete_task(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todo_list'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    todo = Todo.query.get_or_404(id)
    if request.method == 'POST':
        todo.task = request.form['task']
        todo.reminder = request.form['reminder']
        todo.due_date = request.form.get('due_date', None)
        todo.due_time = request.form.get('due_time', None)
        todo.due_date = datetime.strptime(todo.due_date, '%Y-%m-%d').date() if todo.due_date else None
        todo.due_time = datetime.strptime(todo.due_time, '%H:%M').time() if todo.due_time else None
        db.session.commit()
        return redirect(url_for('todo_list'))
    return render_template('edit_task.html', todo=todo)

if __name__ == '__main__':
    app.run(debug=True)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

