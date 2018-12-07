from datetime import date

from django.test import TestCase
from django.core.exceptions import ValidationError

from insurance.models import (
    Risk,
    RiskType,
    TextField,
    NumberField,
    DateField,
    EnumField,
    UnknownField
)


class RiskTypeTest(TestCase):
    def test_fields_can_be_added_to_a_risk_type(self):
        car = RiskType.objects.create(name='car')
        TextField.objects.create(risk_type=car, label='Brand', pos=1)
        NumberField.objects.create(risk_type=car, label='Year', pos=2)
        DateField.objects.create(risk_type=car, label='Release Date', pos=3)
        fuel_types = ['Gasoline', 'Diesel', 'Ethanol']
        EnumField.objects.create(
            risk_type=car, label='Fueled By', pos=4, choices=fuel_types
        )


class RiskTypeFieldTest(TestCase):
    def test_enum_field_choices_must_be_specified(self):
        risk_type = RiskType.objects.create(name='car')
        with self.assertRaises(ValidationError):
            EnumField.objects.create(
                risk_type=risk_type, label='Fuel', pos=1
            )


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

    def test_risk_enum_field_values_can_be_set(self):
        # GIVEN
        risk_type = RiskType.objects.create(name='car')
        EnumField.objects.create(
            risk_type=risk_type,
            label='Fuel',
            pos=1,
            choices=['Gasoline', 'Diesel'],
        )

        # WHEN
        risk = risk_type.new_value()
        risk.set_field_value(field_label='Fuel', value='Gasoline')

        # THEN
        new_risk_instance = Risk.objects.get(id=risk.id)
        self.assertEqual(
            'Gasoline', new_risk_instance.fields['Fuel']
        )

    def test_risk_enum_field_value_must_be_a_valid_choice(self):
        # GIVEN
        risk_type = RiskType.objects.create(name='car')
        EnumField.objects.create(
            risk_type=risk_type,
            label='Fuel',
            pos=1,
            choices=['Gasoline', 'Diesel'],
        )

        # WHEN
        risk = risk_type.new_value()
        with self.assertRaises(ValidationError):  # THEN
            risk.set_field_value(field_label='Fuel', value='Hydrogen')

    def test_raises_exception_setting_values_for_unknown_field(self):
        # GIVEN
        risk_type = RiskType.objects.create(name='car')

        # WHEN
        risk = risk_type.new_value()

        # THEN
        with self.assertRaises(UnknownField):
            risk.set_field_value(field_label='not a field', value='')
