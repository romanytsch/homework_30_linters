"""
Для каждого поля и валидатора в эндпоинте /registration напишите юнит-тест,
который проверит корректность работы валидатора. Таким образом, нужно проверить, что существуют
наборы данных, которые проходят валидацию, и такие, которые валидацию не проходят.
"""

import unittest
from hw1_registration import app

class RegistrationFormTest(unittest.TestCase):

    def setUp(self):
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_email_valid(self):
        data = {
            "email": "test@mail.ru",
            "phone": "1234567890",
            "name": "User",
            "adress": "My address",
            "index": "12345",
            "comment": ""
        }
        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 200)

    def test_email_invalid(self):
        data = {
            "email": "invalid_email",
            "phone": "1234567890",
            "name": "User",
            "adress": "My address",
            "index": "12345",
            "comment": ""
        }
        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 400)

    def test_phone_valid(self):
        data = {
            "email": "test@mail.ru",
            "phone": "1234567890",
            "name": "User",
            "adress": "My address",
            "index": "12345",
            "comment": ""
        }
        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 200)

    def test_phone_invalid(self):
        data = {
            "email": "test@mail.ru",
            "phone": "12345",
            "name": "User",
            "adress": "My address",
            "index": "12345",
            "comment": ""
        }
        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 400)


    def test_name_valid(self):
        data = {
            "email": "test@mail.ru",
            "phone": "1234567890",
            "name": "Valid_name",
            "adress": "My address",
            "index": "12345",
            "comment": ""
        }
        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 200)


    def test_name_invalid(self):
        data = {
            "email": "test@mail.ru",
            "phone": "1234567890",
            "name": "",
            "adress": "My address",
            "index": "12345",
            "comment": ""
        }
        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 400)

    def test_address_valid(self):
        data = {
            "email": "test@mail.ru",
            "phone": "1234567890",
            "name": "Valid_name",
            "adress": "Valid_address",
            "index": "12345",
            "comment": ""
        }
        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 200)


    def test_address_invalid(self):
        data = {
            "email": "test@mail.ru",
            "phone": "1234567890",
            "name": "Valid_name",
            "adress": "",
            "index": "12345",
            "comment": ""
        }
        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 400)


    def test_index_valid(self):
        data = {
            "email": "test@mail.ru",
            "phone": "1234567890",
            "name": "Valid_name",
            "adress": "My address",
            "index": "12345",
            "comment": ""
        }
        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 200)

    def test_index_invalid(self):
        data = {
            "email": "test@mail.ru",
            "phone": "1234567890",
            "name": "Valid_name",
            "adress": "My address",
            "index": "12345acb",
            "comment": ""
        }
        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 400)


    def test_comment_optional(self):
        data = {
            "email": "test@mail.ru",
            "phone": "1234567890",
            "name": "Valid_name",
            "adress": "My address",
            "index": "12345",
            "comment": ""
        }
        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
