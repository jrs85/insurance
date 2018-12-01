from insurance.models import RiskType
from rest_framework import viewsets
from insurance.serializers import RiskTypeSerializer


class RiskTypeViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = RiskType.objects.all()
    serializer_class = RiskTypeSerializer
