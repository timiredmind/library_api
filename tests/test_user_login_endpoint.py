import unittest
from app import create_app
from extension import db
from http import HTTPStatus


class TestUserLoginEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    #     Register user
        user_detail = {
            "username": "timiredmind",
            "email": "timulehinoladokun@gmail.com",
            "password": "goodness4321"
        }
        response = self.client.post("/users/register", json=user_detail)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_endpoint_case1(self):
        login_credentials = {
            "username": "timiredmind",
            "password": "goodness4321"
        }
        response = self.client.post("/login", json=login_credentials)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("access_token", response.json)

    def test_login_endpoint_case2(self):
        login_credentials = {
            "username": "timi_redmind",
            "password": "goodness4321"
        }
        response = self.client.post("/login", json=login_credentials)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(response.json, "Invalid username or password.")

    def test_login_endpoint_case3(self):
        login_credentials = {
            "username": "timiredmind",
            "password": "goodness"
        }
        response = self.client.post("/login", json=login_credentials)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(response.json, "Invalid username or password.")

    def test_login_endpoint_case4(self):
        login_credentials = {
            "username": "timiredmind",
            "email": "timulehinoladokun@gmail.com"
        }
        response = self.client.post("/login", json=login_credentials)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json["errors"]["password"], ["Missing data for required field."])

    def test_login_endpoint_case5(self):
        login_credentials = {
            "username": "timiredmind",
            "password": "goodness4321"
        }
        response = self.client.get("/login", json=login_credentials)
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        self.assertDictEqual(response.json, {"message": "The method is not allowed for the requested URL."})


if __name__ == '__main__':
    unittest.main()
