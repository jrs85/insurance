from insurance import models
from insurance.models import (
    RiskType,
    RiskTypeField,
    TextField,
    NumberField,
    DateField,
    EnumField,
)
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer


class RiskTypeFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskTypeField
        fields = ('id', 'label', 'pos', 'field_type')


class EnumFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnumField
        fields = ('id', 'label', 'pos', 'field_type', 'choices')


class RiskTypeFieldPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        RiskTypeField: RiskTypeFieldSerializer,
        EnumField: EnumFieldSerializer,
        TextField: RiskTypeFieldSerializer,
        DateField: RiskTypeFieldSerializer,
        NumberField: RiskTypeFieldSerializer,
    }


class RiskTypeSerializer(serializers.HyperlinkedModelSerializer):
    fields = RiskTypeFieldPolymorphicSerializer(
        many=True, read_only=False, required=True
    )

    class Meta:
        model = RiskType
        fields = ('id', 'url', 'name', 'fields')

    def create(self, validated_data):
        fields = validated_data.pop('fields', [])
        risk_type = RiskType.objects.create(**validated_data)
        for f in fields:
            field_type = f.pop('resourcetype')
            getattr(models, field_type).objects.create(
                risk_type=risk_type, **f
            )
        return risk_type
