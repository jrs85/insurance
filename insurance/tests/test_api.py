from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from insurance import models


class RiskTypeApiTests(APITestCase):
    def test_create_risk_type(self):
        url = reverse('risktype-list')
        data = {'name': 'Car'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, models.RiskType.objects.count())
        self.assertEqual('Car', models.RiskType.objects.get().name)

    def test_get_risk_type_fields(self):
        # GIVEN a risk type with 2 fields
        risk_type = models.RiskType.objects.create(name='car')
        models.TextField.objects.create(
            risk_type=risk_type, label='Brand', pos=1
        )
        models.TextField.objects.create(
            risk_type=risk_type, label='Model', pos=2
        )
        # WHEN
        url = reverse('risktype-detail', args=[risk_type.id])
        response = self.client.get(url, format='json')

        # THEN
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = response.json()
        self.assertEqual('car', response['name'])
        self.assertEqual(2, len(response['fields']))

        brand = response['fields'][0]
        self.assertTrue('Brand', brand['label'])
        self.assertTrue(1, brand['pos'])
        self.assertTrue('text', brand['field_type'])
        self.assertTrue('id' in brand)
