from datetime import date

from django.test import TestCase
from django.core.exceptions import ValidationError

from insurance.models import (
    Risk,
    RiskType,
    TextField,
    NumberField,
    DateField,
)


class RiskTypeTest(TestCase):
    def test_fields_can_be_added_to_a_risk_type(self):
        car = RiskType(name='car')
        car.save()
        brand_field = TextField(risk_type=car, label='Brand', pos=1)
        brand_field.save()


class RiskTest(TestCase):
    def test_risk_text_field_values_can_be_set(self):
        # GIVEN
        risk_type = RiskType.objects.create(name='car')
        TextField.objects.create(risk_type=risk_type, label='Brand', pos=1)

        # WHEN
        risk = risk_type.new_value()
        risk.set_field_value(field_label='Brand', value='BMW')

        # THEN
        new_risk_instance = Risk.objects.get(id=risk.id)
        self.assertEqual('BMW', new_risk_instance.fields['Brand'])

    def test_risk_number_field_values_can_be_set(self):
        # GIVEN
        risk_type = RiskType.objects.create(name='car')
        NumberField.objects.create(risk_type=risk_type, label='Year', pos=1)
        NumberField.objects.create(risk_type=risk_type, label='Price', pos=2)

        # WHEN
        risk = risk_type.new_value()
        risk.set_field_value(field_label='Year', value=2015)
        risk.set_field_value(field_label='Price', value=1000.50)

        # THEN
        new_risk_instance = Risk.objects.get(id=risk.id)
        self.assertEqual(2015, new_risk_instance.fields['Year'])
        self.assertEqual(1000.50, new_risk_instance.fields['Price'])

    def test_number_fields_can_only_store_numeric_values(self):
        # GIVEN
        risk_type = RiskType.objects.create(name='car')
        NumberField.objects.create(risk_type=risk_type, label='Year', pos=1)

        # WHEN
        risk = risk_type.new_value()

        # THEN
        with self.assertRaises(ValidationError):
            risk.set_field_value(field_label='Year', value='str value')

    def test_risk_date_field_values_can_be_set(self):
        # GIVEN
        risk_type = RiskType.objects.create(name='painting')
        DateField.objects.create(
            risk_type=risk_type, label='Created on', pos=1
        )

        # WHEN
        risk = risk_type.new_value()
        risk.set_field_value(field_label='Created on', value='2010-10-23')

        # THEN
        new_risk_instance = Risk.objects.get(id=risk.id)
        self.assertEqual(
            date(2010, 10, 23), new_risk_instance.fields['Created on']
        )
