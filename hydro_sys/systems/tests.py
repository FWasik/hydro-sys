from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import HydroponicSystem, Measurement

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

        self.client.force_authenticate(user=self.user)


class HydroponicSystemTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.systems = [
            HydroponicSystem.objects.create(
                name=f"System {i}", owner=self.user, type="NFT"
            )
            for i in range(15)
        ]
        HydroponicSystem.objects.create(name=f"System 15", owner=self.user, type="Wick")

        self.url = reverse("hydroponic-list")

    def test_create_system_success(self):
        payload = {"name": "New System", "type": "Drip"}

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_system_invalid(self):
        payload = {"name": "New System", "type": "Invalid type"}

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_system(self):
        system = self.systems[0]
        payload = {
            "name": "Updated Name",
            "type": "Aeroponics",
        }

        response = self.client.patch(f"{self.url}{system.id}/", payload, format="json")
        system.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(system.name, "Updated Name")

    def test_delete_system(self):
        system = self.systems[1]

        response = self.client.delete(f"{self.url}{system.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(HydroponicSystem.objects.filter(id=system.id).exists())

    def test_pagination_system(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 10)
        self.assertIsNotNone("next", response.data.get("next"))

    def test_ordering_system(self):
        response = self.client.get(self.url + "?ordering=name")

        expected = [
            system.name for system in HydroponicSystem.objects.all().order_by("name")
        ][:10]
        result = [obj.get("name") for obj in response.data.get("results")]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected, result)

    def test_filtering_by_type_system(self):
        response = self.client.get(self.url + "?type=Wick")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 1)

    def test_unauthorized_action(self):
        self.client.force_authenticate(user=self.other_user)
        system = self.systems[0]

        response = self.client.get(f"{self.url}{system.id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class MeasurementTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.system = HydroponicSystem.objects.create(
            name="Test System", owner=self.user, type="NFT"
        )

        self.measurements = [
            Measurement.objects.create(
                system=self.system, ph=6.5, temperature=22, tds=500
            )
            for _ in range(12)
        ]

        Measurement.objects.create(
            system=self.system, ph=10, temperature=5.5, tds=302.20
        )
        Measurement.objects.create(
            system=self.system, ph=9.2, temperature=10, tds=234.32
        )
        Measurement.objects.create(
            system=self.system, ph=3.4, temperature=15.3, tds=453.24
        )

        self.url = reverse("measurement-list")

    def test_create_measurement_success(self):
        payload = {
            "system": self.system.name,
            "ph": 12.0,
            "temperature": 20,
            "tds": 500,
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_measurement_invalid(self):
        payload = {
            "system": "some_invalid_name",
            "ph": 15.0,
            "temperature": 1005,
            "tds": -20,
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_measurement(self):
        measurement = self.measurements[0]
        payload = {
            "system": self.system.name,
            "ph": 5.0,
            "temperature": 20,
            "tds": 300,
        }

        response = self.client.patch(
            f"{self.url}{measurement.id}/", payload, format="json"
        )
        measurement.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(measurement.ph, 5.0)
        self.assertEqual(measurement.temperature, 20)
        self.assertEqual(measurement.tds, 300)

    def test_delete_measurement(self):
        measurement = self.measurements[1]

        response = self.client.delete(f"{self.url}{measurement.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Measurement.objects.filter(id=measurement.id).exists())

    def test_pagination_measurement(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 10)
        self.assertIsNotNone("next", response.data)

    def test_ordering_measurement(self):
        response = self.client.get(self.url + "?ordering=ph")

        expected = [
            measurement.ph for measurement in Measurement.objects.all().order_by("ph")
        ][:10]
        result = [obj.get("ph") for obj in response.data.get("results")]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected, result)

    def test_filtering_measurement(self):
        url = (
            self.url
            + "?ph_min=3.4&ph_max=10&temperature_min=5.5&temperature_max=15.3&tds_min=234.32&tds_max=453.24"
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 3)

    def test_unauthorized_action(self):
        self.client.force_authenticate(user=self.other_user)
        measurement = self.measurements[0]

        response = self.client.get(f"{self.url}{measurement.id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
