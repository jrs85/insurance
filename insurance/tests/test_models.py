from django.test import TestCase
from insurance import models


class RiskTypeTest(TestCase):
    def test_fields_can_be_added_to_a_risk_type(self):
        car = models.RiskType(name='car')
        car.save()
        brand_field = models.TextField(risk_type=car, label='Brand', pos=1)
        brand_field.save()


class RiskTest(TestCase):
    def test_risk_text_field_values_can_be_set(self):
        # GIVEN
        risk_type = models.RiskType(name='car')
        risk_type.save()
        brand_field = models.TextField(
            risk_type=risk_type, label='Brand', pos=1
        )
        brand_field.save()

        # WHEN
        risk = risk_type.new_value()
        risk.set_field_value(field_label='Brand', value='BMW')

        # THEN
        new_risk_instance = models.Risk.objects.get(id=risk.id)
        self.assertEqual('BMW', new_risk_instance.fields['Brand'])
