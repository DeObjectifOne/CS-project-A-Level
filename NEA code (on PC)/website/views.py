from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Task
from . import db
import json #used to translate the javascript in index.js to pythonic code
from datetime import datetime
from .__init__ import SearchForm


views = Blueprint('views', __name__)

#used redirect the user to the default page (home page)
@views.route('/', methods=['GET', 'POST'])
@login_required #put in place so the user can't access the home page until they've logged in
def home():
    if request.method == 'POST':
        #retrieves all task data
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
        db.session.add(new_task) #adds the task and its relevent data to the database
        db.session.commit()
        flash('Task added successfully', category='success')
        
    #search form routes
    form = SearchForm()
    tasks = []

    if request.method == 'POST':
         if form.validate_on_submit():
            search_query = form.search_query.data
            tasks = Task.query.filter(
                Task.task.ilike(f"%{search_query}%"),
                Task.user_id == current_user.id,
            ).all()

            flash(f'Search for: {search_query}', 'The search has been successful')
    else:
        tasks = Task.query.filter_by(user_id=current_user.id).all()
    
    return render_template("home.html", user=current_user, form=form, tasks=tasks)

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