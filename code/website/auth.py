from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User


#used to create a WSGI (Web Server Gateway Interference) that handles user requests
from werkzeug.security import generate_password_hash, check_password_hash

#imports the database to store user data from login and sign up
from . import db

#used to handle data from the user
from flask_login import login_user, login_required, logout_user, current_user

#imports to allow the app to send emails to its users
import smtplib
import os
from dotenv import load_dotenv

auth = Blueprint('auth', __name__)

#loads content from my env file
load_dotenv()

#route used for the login function
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Login successful', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password incorrect, please try again', category='error')
        else:
            flash('The user does not exist, please input a different email', category='error')
                

    return render_template("login.html", user=current_user)

#route used for the logout function
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login')) #used to redirect the user back to the login page


#route used for the sign up function
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #used to find if the user already exists in the database
        user = User.query.filter_by(email=email).first()

        #password validation
        if user:
            flash('A user with this email already exists, please input a different email', category='error')
        elif len(password1) < 8:
            flash('The password length cannot be shorter than 8 characters', category='error')
        elif password1 != password2:
            flash('The passwords do not match', category='error')
        else:
            new_user = User(email=email, fullname=fullname, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Accounted created successfully', category='success')
            registration_email(email)
            return redirect(url_for('views.home'))

    return render_template("sign-up.html", user=current_user)

def registration_email(to_email):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_email = 'ethan.tongson1806@gmail.com'
    smtp_password = os.getenv("SMTP_PASSWORD")

    #checking to see if the SMTP password is set
    if not smtp_password:
        print("Environment variable 'SMTP_PASSWORD' is not set.")
        return "An error occured with configuring the email."
    
    #email contents
    subject = "Registration successful"
    body = f"Hello, you have been successfully registered into the Diddly Day Tracker!"
    message = f"Subject: {subject}\n\n{body}"

    try:
        #server setup
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_email, smtp_password)

        #sending the email
        server.sendmail(smtp_email, to_email, message)
        print("An email has been sent to the user successfully")
    except Exception as e:
        print(f"Failed to send an email: {e}")
    finally:
        server.quit()