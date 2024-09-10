from rest_framework import serializers
from apps.stb_tester.models import StbResult


class ResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = StbResult
        fields = ('result_url', 'result', 'failure_reason')
