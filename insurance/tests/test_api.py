from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from insurance.models import RiskType


class RiskTypeApiTests(APITestCase):
    def test_create_risk_type(self):
        url = reverse('risktype-list')
        data = {'name': 'Car'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RiskType.objects.count(), 1)
        self.assertEqual(RiskType.objects.get().name, 'Car')
