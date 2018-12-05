from django.db import models
from django.core.exceptions import ValidationError

import jsonfield

from polymorphic.models import PolymorphicModel


class UnknownField(Exception):
    pass


# TODO add user id or assume each customer will have their own instance


class RiskType(models.Model):
    name = models.CharField(max_length=100)

    def new_value(self):
        r = Risk(risk_type=self)
        r.save()
        return r

    def __str__(self):
        return self.name


class Risk(models.Model):
    risk_type = models.ForeignKey(RiskType, on_delete=models.PROTECT)

    def set_field_value(self, field_label, value):
        fields = self.risk_type.fields.all()
        for f in fields:
            if f.label == field_label:
                v = f.new_value_for(self, value)
                v.save()
                return
        raise UnknownField(
            f'No field with "{field_label}" label could be found for '
            f'the {self.risk_type.name} RiskType'
        )

    @property
    def fields(self):
        return {
            f.field.label: f.value
            for f in self.value_set.all()
        }


class RiskTypeField(PolymorphicModel):
    risk_type = models.ForeignKey(
        RiskType, on_delete=models.CASCADE, related_name='fields'
    )
    label = models.CharField(max_length=100)
    pos = models.IntegerField()
    field_type = 'abstract'

    def new_value_for(self, risk, value):
        raise NotImplementedError()


class TextField(RiskTypeField):
    field_type = 'text'

    def new_value_for(self, risk, value):
        return TextValue(field=self, risk=risk, value=value)


class NumberField(RiskTypeField):
    field_type = 'number'

    def new_value_for(self, risk, value):
        return NumberValue(field=self, risk=risk, value=value)


class DateField(RiskTypeField):
    field_type = 'date'

    def new_value_for(self, risk, value):
        return DateValue(field=self, risk=risk, value=value)


class EnumField(RiskTypeField):
    field_type = 'enum'
    choices = jsonfield.JSONField()

    def new_value_for(self, risk, value):
        if value not in self.choices:
            raise ValidationError(
                f'`{value}` is not a valid choice for the {self.label} '
                f'EnumField. Available options: {self.choices}'
            )
        return EnumValue(field=self, risk=risk, value=value)

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if not self.choices:
            raise ValidationError(
                'The `choices` field must be defined for EnumField'
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Value(PolymorphicModel):
    field = models.ForeignKey(RiskTypeField, on_delete=models.CASCADE)
    risk = models.ForeignKey(Risk, on_delete=models.CASCADE)


class TextValue(Value):
    value = models.CharField(max_length=100)


class NumberValue(Value):
    value = models.DecimalField(max_digits=15, decimal_places=2)


class DateValue(Value):
    value = models.DateField()


class EnumValue(Value):
    value = models.CharField(max_length=100)
