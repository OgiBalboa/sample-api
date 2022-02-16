from rest_framework import serializers
from api.models import PerformanceMetrics


class PerformanceMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceMetrics
        fields = '__all__'


class PerformanceMetricsListSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return instance
