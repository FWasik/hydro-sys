from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user",
            email="test_email@email.com",
            password="test_pass",
            phone_number="123456789",
        )
        self.other_user = User.objects.create_user(
            username="other_user",
            email="other_email@email.com",
            password="test_pass",
            phone_number="987654321",
        )
