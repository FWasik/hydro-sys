from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from tests.base import BaseTestCase

User = get_user_model()


class UserTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.url = reverse("token_obtain_pair")

    def test_get_tokens_success(self):
        payload = {"username": "test_user", "password": "test_pass"}

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_tokens_invalid(self):
        payload = {"username": "invalid_user", "password": "invalid_pass"}

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
