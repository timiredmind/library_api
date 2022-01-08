import unittest
from app import create_app
from http import HTTPStatus
from extension import db


class TestUserProfileEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        user_detail = {
            "username": "timiredmind",
            "email": "timulehinoladokun@gmail.com",
            "password": "goodness4321"
        }
        response = self.client.post("/users/register", json=user_detail)
        self.token = response.json["access_token"]

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_profile_endpoint_case1(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = self.client.get("/users/profile", headers=headers)
        json_response = response.json
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(json_response["id"], 1)
        self.assertEqual(json_response["username"], "timiredmind")
        self.assertEqual(json_response["email"], "timulehinoladokun@gmail.com")

    def test_user_profile_endpoint_case2(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = self.client.post("/users/profile", headers=headers)
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_user_profile_endpoint_case3(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        new_details = {
            "username": "timi",
            "email": "joshua_oladokun@yahoo.com"
        }
        response = self.client.patch(
            "/users/profile",
            headers=headers,
            json=new_details)
        json_data = response.json
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(json_data["id"], 1)
        self.assertEqual(json_data["username"], "timi")
        self.assertEqual(json_data["email"], "joshua_oladokun@yahoo.com")

    def test_user_profile_endpoint_case4(self):
        new_user = {
            "username": "joshua",
            "email": "joshua_oladokun@yahoo.com",
            "password": "joshua"
        }
        self.client.post("/users/register", json=new_user)

        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        new_username = {
            "username": "joshua"
        }
        response = self.client.patch(
            "/users/profile",
            headers=headers,
            json=new_username)
        self.assertEqual(response.status_code, HTTPStatus.CONFLICT)
        self.assertEqual(
            response.json["message"],
            "Username already associated with a different user.")

    def test_user_profile_endpoint_case5(self):
        new_user = {
            "username": "joshua",
            "email": "joshua_oladokun@yahoo.com",
            "password": "joshua"
        }
        self.client.post("/users/register", json=new_user)

        headers = {
            "Authorization": f"Bearer {self.token}"}

        new_email = {
            "email": "joshua_oladokun@yahoo.com"
        }
        response = self.client.patch(
            "/users/profile",
            headers=headers,
            json=new_email)
        self.assertEqual(response.status_code, HTTPStatus.CONFLICT)
        self.assertEqual(
            response.json["message"],
            "Email address associated with a different user.")


if __name__ == '__main__':

    unittest.main()
