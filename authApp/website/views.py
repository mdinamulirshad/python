
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from website.models import City, Employee
from . import db
from flask_wtf import FlaskForm
from wtforms import RadioField



views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    all_employee = Employee.query.all()

    return render_template("home.html", user=current_user, employees=all_employee)


@views.route('/addNewEmployee', methods=['GET', 'POST'])
def addNewEmployee():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        new_employee = Employee(name=name, email=email, phone=phone, user_id=current_user.id)
        db.session.add(new_employee)
        db.session.commit()
        flash('Employee Added.', category='success')
        return redirect(url_for('views.home'))

    return redirect(url_for('views.home'),user=current_user)


@views.route('/editEmployee', methods=['GET', 'POST'])
def editEmployee():
    if request.method == 'POST':
        employees = Employee.query.get(request.form.get('id'))

        employees.name = request.form.get('name')
        employees.email = request.form.get('email')
        employees.phone = request.form.get('phone')
        db.session.commit()
        return redirect(url_for('views.home'))

    return redirect(url_for('views.home'))


@views.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    employees = Employee.query.get(id)
    db.session.delete(employees)
    db.session.commit()
    flash('Employee Deletd Successfully.', category='success')
    return redirect(url_for('views.home'))


# DYNAMIC FORM FIELD USING WT_FORMS 

class Form(FlaskForm):
    state = RadioField('state', choices=[('CA',"California"),('NV','Nevada')])
    city = RadioField('city', choices=[])

@views.route('/index', methods=['GET', 'POST'])
def index():
    form = Form()
    form.city.choices = [(city.id, city.name) for city in City.query.filter_by(state='CA').all()]

    return render_template('index.html', user=current_user, form=form)


@views.route('/city/<state>')
def city(state):
    cities = City.query.filter_by(state=state).all()

    cityArray = []
    for city in cities:
        cityObj ={}
        cityObj['id'] = city.id
        cityObj['name'] = city.name
        cityArray.append(cityObj)

    return jsonify({'cities' : cityArray})
