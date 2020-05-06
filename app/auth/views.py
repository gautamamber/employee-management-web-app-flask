from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from app.models import Employee


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register userin employee database
    :return:
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        employee = Employee(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)
        db.session.add(employee)
        db.session.commit()
        flash("Successfully register")
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    user login
    First check employee exists in database and then match password
    :return:
    """
    form = LoginForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee is not None and employee.verify_password(form.password.data):
            login_user(employee)
            if employee.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))
        else:
            flash("Email or password is incorrect")

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """
    User log out
    :return:
    """
    logout_user()
    flash("User is successfully logout")
    return redirect(url_for('auth.login'))
