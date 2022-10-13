
from unicodedata import category
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

from .generateOtp import generateOTP

import os
from twilio.rest import Client




auth = Blueprint('auth', __name__)

@auth.route('/signUp', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        print(phone)

        # Otp verification
        status = sendOtpApi(phone)

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif password != password2:
            flash('Password did not match..', category='error')
        else:
            status == True

            session['email'] = email
            session['phone'] = phone
            session['password'] = password

            flash('Account created!', category='success')
            # return redirect(url_for('views.home'))
            return redirect(url_for('auth.enterOtp'))

    return render_template('signup.html', user=current_user)




@auth.route('/enterOtp', methods=['GET', 'POST'])
def enterOtp():
    if request.method == 'POST':
        otp = request.form.get('otp')

        # Saving  New User In Database
        email = session['email']
        phone = session['phone']
        password = session['password']
        new_user = User(email=email, phone=phone, password=generate_password_hash(password, method='sha256'))
        if "response" in session:
            s = session['response']
            session.pop('respose', None)
            if s == otp:
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Worng Otp!', category='error')
                return 'worng Otp'

    return render_template('enterOtp.html')



def sendOtpApi(phone):
    otp = generateOTP()
    msg = "Your OTP is " + otp
    session['response'] = str(otp)

    account_sid = "AC02f936a0c89161a491cf178c8132d477"
    auth_token = "d8887de31b56976912c21dfd84cfe7ae"
    client = Client(account_sid, auth_token)

    message = client.messages.create(from_="+17866487813", body=msg, to=phone)

    if message.sid:
        return True
    else:
        False

    print(message.body)




@auth.route('/logIn', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/logOut')
@login_required
def logOut():
    logout_user()
    return redirect(url_for('auth.login'))