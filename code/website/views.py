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
        task = request.form.get('task')

        new_task = Task(data=task, user_id=current_user.id)
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