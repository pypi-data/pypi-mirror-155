from rest_framework import serializers


class MonitoringViewSetSerializer(serializers.Serializer):
    result = serializers.BooleanField()
