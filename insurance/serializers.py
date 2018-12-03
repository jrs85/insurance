from insurance.models import (
    RiskType,
    RiskTypeField,
)
from rest_framework import serializers


class RiskTypeFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskTypeField
        fields = ('id', 'label', 'pos', 'field_type')


class RiskTypeSerializer(serializers.HyperlinkedModelSerializer):
    fields = RiskTypeFieldSerializer(many=True, read_only=True)

    class Meta:
        model = RiskType
        fields = ('id', 'url', 'name', 'fields')
