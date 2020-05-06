from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from . import admin
from forms import DepartmentForm
from .. import db
from app.models import Department


def check_admin():
    """
    Prevent non admin users to access the page
    :return:
    """
    if not current_user.is_admin:
        abort(403)


@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
    """
    List all departments
    :return:
    """
    check_admin()
    departments = Department.query.all()
    return render_template('admin/departments/departments.html', departments=departments, title='Departments')


@admin.route('/departments/add', methods=['POST', 'GET'])
@login_required
def add_department():
    """
    Add department
    :return:
    """
    check_admin()
    department_add = True
    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data, description=form.description.data)
        try:
            db.session.add(department)
            db.session.commit()
            flash("Department added successfully")
        except:
            flash("Already exists")
    return render_template('admin/departments/department.html', action="Add",
                           department_add=department_add, form=form,
                           title="Add Department")


