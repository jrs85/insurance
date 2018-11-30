from django.db import models

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


class Risk(models.Model):
    risk_type = models.ForeignKey(RiskType, on_delete=models.PROTECT)

    def set_field_value(self, field_label, value):
        fields = self.risk_type.risktypefield_set.all()
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
    risk_type = models.ForeignKey(RiskType, on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    pos = models.IntegerField()

    def new_value_for(self, risk, value):
        raise NotImplementedError()


class TextField(RiskTypeField):
    def new_value_for(self, risk, value):
        return TextValue(field=self, risk=risk, value=value)


class Value(PolymorphicModel):
    field = models.ForeignKey(RiskTypeField, on_delete=models.CASCADE)
    risk = models.ForeignKey(Risk, on_delete=models.CASCADE)


class TextValue(Value):
    value = models.CharField(max_length=100)
