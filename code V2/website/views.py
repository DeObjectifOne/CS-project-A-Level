from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Task
from . import db
import json


views = Blueprint('views', __name__)

#used redirect the user to the default page (home page)
@views.route('/', methods=['GET', 'POST'])
@login_required #put in place so the user can't access the home page until they've logged in
def home():
    if request.method == 'POST':
        #retrieves all task data
        title = request.form.get('title')
        task = request.form.get('task')
        duration = request.form.get('duration')
        completion_date = request.form.get('completion_date')
        priority = request.form.get('priority')

        new_task = Task(
            title=title,
            data=task, 
            duration=duration, 
            completion_date=completion_date, 
            priority=priority, 
            user_id=current_user.id
        )
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully', category='success')
        
    return render_template("home.html", user=current_user)

#handles task deletion after the user sends a POST request
@views.route('/delete-task', methods=['POST'])
def delete_task():
    task = json.loads(request.data)
    taskId = task['taskId']
    task = Task.query.get(taskId)
    if task:
        if task.user_id == current_user.id:
            db.session.delete(task)
            db.session.commit()
    
    return jsonify({})