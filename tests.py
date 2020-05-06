import unittest
from flask import abort, url_for
from flask_testing import TestCase
from app import create_app, db
from app.models import Employee, Role, Department


class TestBase(TestCase):
    """
    Base class for test cases
    """

    def create_app(self):
        """
        pass test config
        :return:
        """
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql://dt_admin:dt2020@localhost/dreamteam_test'
        )
        return app

    def setUp(self):
        """
        Call this before every test
        :return:
        """
        db.create_all()
        # create test admin user
        admin = Employee(username='admin', password='admin202', is_admin=True)
        employee = Employee(username="test_user", password="test2016")
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()

    def tearDown(self):
        """
        clear database remove after every test case
        :return:
        """
        db.session.remove()
        db.drop_all()


class TestModels(TestBase):
    """
    Test models
    """

    def test_employee_model(self):
        """
        Test employee model, count number of records
        :return:
        """
        self.assertEqual(Employee.query.count(), 2)

    def test_department_model(self):
        """
        test department model, count number records
        :return:
        """
        department = Department(name="IT", description="It department")
        db.session.add(department)
        db.session.commit()
        self.assertEqual(Department.query.count(), 1)

    def test_role_model(self):
        """
        test department model, count number records
        :return:
        """
        role = Role(name="CEO", description="CEO role")
        db.session.add(role)
        db.session.commit()
        self.assertEqual(Role.query.count(), 1)


if __name__ == "__main__":
    unittest.main()
