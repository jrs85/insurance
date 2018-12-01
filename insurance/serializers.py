from insurance.models import RiskType
from rest_framework import serializers


class RiskTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RiskType
        fields = ('url', 'name')
