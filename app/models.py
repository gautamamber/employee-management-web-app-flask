from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


class Employee(UserMixin, db.Model):
    """
    Create Employee Table
    Ensure name will be in plural
    """
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(50), index=True)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent password for being accessed
        :return:
        """
        raise AttributeError("Password is not readable attribute")

    def verify_password(self, password):
        """
        check if hashed password is matches actual password
        :param password:
        :return:
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """

        :return:
        """
        return 'Employee: {}'.format(self.username)


@login_manager.user_loader
def load_user(user_id):
    """
    Set up a user loader
    Flask-Login uses to reload the user object from the user ID stored in the session.
    :param user_id:
    :return:
    """
    return Employee.query.get(int(user_id))


class Department(db.Model):
    """
    Create a department table
    """
    __tablename__ = "departments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='department',
                                lazy='dynamic')

    def __repr__(self):
        """

        :return:
        """
        return "Department: {}".format(self.name)


class Role(db.Model):
    """
    Role Table
    """
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        """

        :return:
        """
        return "Role: {}".format(self.name)
