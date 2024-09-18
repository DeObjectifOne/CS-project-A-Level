from flask import Blueprint, render_template, request, flash, jsonify, session
from flask_login import login_required, current_user
from .models import Task
from . import db
import json
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        task = request.form.get('task')
        details = request.form.get('details')
        duration = request.form.get('duration')
        completion_date_str = request.form.get('completion_date')
        completion_date = datetime.strptime(completion_date_str, '%Y-%m-%dT%H:%M')
        priority = request.form.get('priority')
        new_task = Task(
            task=task,
            data=details,
            duration=duration,
            completion_date=completion_date,
            priority=priority,
            user_id=current_user.id
        )
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully', category='success')
    return render_template("home.html", user=current_user)

@views.route('/delete-task', methods=['POST'])
def delete_task():
    task = json.loads(request.data)
    taskId = task['taskId']
    task = Task.query.get(taskId)
    if task and task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
    return jsonify({})

@views.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template("settings.html", user=current_user)

@views.route('/save-mode', methods=['POST'])
@login_required
def save_mode():
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported Media Type"}), 415

    data = request.get_json()
    mode = data.get('mode', 'light')
    session['mode'] = mode
    return jsonify({"message": "Mode saved successfully"})

@views.route('/get-mode', methods=['GET'])
def get_mode():
    #this defaults to light mode if dark mode isn't selected
    mode = session.get('mode', 'light')
    # Return the saved mode
    return jsonify({"mode": mode})
