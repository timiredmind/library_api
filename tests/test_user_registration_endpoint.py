import unittest
from app import create_app
from extension import db
from http import HTTPStatus


class TestUserRegisterEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()  # Bind application context with current context
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()  # Remove application context

    def test_user_registration_case1(self):
        '''Test for complete user registration.'''
        user_detail = {
            "username": "timiredmind",
            "password": "goodness4321",
            "email": "timulehinoladokun@gmail.com"
        }
        response = self.client.post("/users/register", json=user_detail)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertIn("access_token", response.json)

    def test_user_registration_case2(self):
        '''Test for bad request from the client with the email address missing from the request.'''
        user_detail = {
            "username": "timiredmind",
            "password": "goodness4321",
        }
        response = self.client.post("/users/register", json=user_detail)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json["message"], "Validation Error")
        self.assertListEqual(
            response.json["errors"]["email"],
            ["Missing data for required field."])

    def test_user_registration_case3(self):
        '''Test for bad request with the password field missing and an unknown field sent with the request'''
        user_detail = {
            "username": "timiredmind",
            "email": "timulehinoladokun@gmail.com",
            "address": "OAU Staff Quarters"
        }
        response = self.client.post("/users/register", json=user_detail)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json["message"], "Validation Error")
        self.assertListEqual(
            response.json["errors"]["password"],
            ["Missing data for required field."])
        self.assertListEqual(
            response.json["errors"]["address"],
            ["Unknown field."])

    def test_user_registration_case4(self):
        ''' Test to register with an already existing username '''
        user_detail_1 = {
            "username": "timiredmind",
            "password": "goodness4321",
            "email": "timulehinoladokun@gmail.com"
        }
        response1 = self.client.post("/users/register", json=user_detail_1)

        user_detail_2 = {
            "username": "timiredmind",
            "password": "goodness",
            "email": "joshua_oladokun@yahoo.com"
        }
        response2 = self.client.post("/users/register", json=user_detail_2)
        self.assertEqual(response2.status_code, HTTPStatus.CONFLICT)
        self.assertDictEqual(
            response2.json, {
                "message": "Invalid username or username is associated to a different user."})

    def test_user_registration_case5(self):
        '''Test for bad request when email field doesn't contain a correct email.'''
        user_detail = {
            "username": "timiredmind",
            "password": "goodness4321",
            "email": "timulehinoladokun"
        }
        response = self.client.post("/users/register", json=user_detail)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertListEqual(
            response.json["errors"]["email"],
            ["Not a valid email address."])

    def test_user_registration_case6(self):
        user_detail = {
            "username": "timiredmind",
            "password": "goodness4321",
            "email": "timulehinoladokun@gmail.com"
        }
        response = self.client.patch("/users/register", json=user_detail)
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        self.assertDictEqual(
            response.json, {
                'message': 'The method is not allowed for the requested URL.'})

    def test_user_registration_case7(self):
        user_detail1 = {
            "username": "timiredmind",
            "password": "goodness4321",
            "email": "timulehinoladokun@gmail.com"
        }
        self.client.post("/users/register", json=user_detail1)

        user_detail2 = {
            "username": "joshua",
            "password": "goodness",
            "email": "timulehinoladokun@gmail.com"
        }
        response = self.client.post("/users/register", json=user_detail2)
        self.assertEqual(response.status_code, HTTPStatus.CONFLICT)
        self.assertDictEqual(
            response.json, {
                "message": "Invalid email address or email address is associated to a different user."})


if __name__ == '__main__':
    unittest.main(verbosity=4)
