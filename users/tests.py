from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email="test@test.com", username="test", password="test")

    def test_user_create(self):
        data = {
            "email": "test_email@yandex.ru",
            "username": "test_username",
            "password": "test_pswd",
        }

        response = self.client.post("/register/", data=data)
        self.assertEqual(response.data.get("username"), "test_username")
