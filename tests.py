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


class TestViews(TestBase):
    """
    Test views
    """

    def test_home_page_views(self):
        """
        test home page
        :return:
        """
        response = self.client.get(url_for('home.homepage'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        """
        test login view
        :return:
        """
        response = self.client.get('auth.login')
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        """
        test logout after login
        :return:
        """
        target_url = url_for('auth.logout')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_404_not_found(self):
        response = self.client.get('/404error')
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
