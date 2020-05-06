import unittest
from flask_testing import TestCase
from app import create_app, db
from app.models import Employee


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
            SQLALCHEMY_DATABASE_URI='mysql://dt_admin:dt2016@localhost/dreamteam_test'
        )
        return app

    def setUp(self):
        """
        Call this before every test
        :return:
        """
        db.creat_all()
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


if __name__ == "__main__":
    unittest.main()
