import schedule
import time
from datetime import datetime
from models import db, Todo
from app import app

def check_reminders():
    with app.app_context():
        now = datetime.now()
        todos = Todo.query.filter(Todo.due_date == now.date(), Todo.due_time == now.time()).all()
        for todo in todos:
            print(f"Reminder: {todo.task} - {todo.reminder}")

# Schedule the reminder check every minute
schedule.every().minute.do(check_reminders)

while True:
    schedule.run_pending()
    time.sleep(1)
