from insurance.models import (
    RiskType,
    RiskTypeField,
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
    }


class RiskTypeSerializer(serializers.HyperlinkedModelSerializer):
    fields = RiskTypeFieldPolymorphicSerializer(many=True, read_only=True)

    class Meta:
        model = RiskType
        fields = ('id', 'url', 'name', 'fields')
