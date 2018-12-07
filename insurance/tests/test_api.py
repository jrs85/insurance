from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from insurance import models


class RiskTypeApiTests(APITestCase):
    def test_create_risk_type(self):
        url = reverse('risktype-list')
        data = {'name': 'Car', 'fields': []}
        response = self.client.post(url, data, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, models.RiskType.objects.count())
        self.assertEqual('Car', models.RiskType.objects.get().name)

    def test_create_risk_type_with_fields(self):
        url = reverse('risktype-list')
        data = {
            'name': 'Car',
            'fields': [{
                'label': 'text field',
                'pos': 1,
                'resourcetype': 'TextField',
            }, {
                'label': 'date field',
                'pos': 2,
                'resourcetype': 'DateField',
            }, {
                'label': 'number field',
                'pos': 3,
                'resourcetype': 'NumberField',
            }, {
                'label': 'enum field',
                'pos': 4,
                'resourcetype': 'EnumField',
                'choices': ['choice 1', 'choice 2'],
            }]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(
            status.HTTP_201_CREATED, response.status_code, response.json()
        )
        response_data = response.json()
        self.assertEqual('Car', response_data['name'])
        self.assertEqual(4, len(response_data['fields']))
        self.assertEqual(
            ['TextField', 'DateField', 'NumberField', 'EnumField'],
            [f['resourcetype'] for f in response_data['fields']]
        )

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

    def test_serialized_enum_fields_contain_the_choices(self):
        # GIVEN a risk type with 2 fields
        risk_type = models.RiskType.objects.create(name='car')
        models.EnumField.objects.create(
            risk_type=risk_type,
            label='Fuel',
            pos=1,
            choices=['Gasoline', 'Diesel'],
        )

        # WHEN
        url = reverse('risktype-detail', args=[risk_type.id])
        response = self.client.get(url, format='json').json()
        api_field = response['fields'][0]
        self.assertTrue('Gasoline' in api_field['choices'])
        self.assertTrue('id' in api_field)
        self.assertEqual('Fuel', api_field['label'])
