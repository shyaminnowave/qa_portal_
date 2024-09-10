from rest_framework import serializers
from apps.stb_tester.models import StbResult


class ResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = StbResult
        fields = ('start_time', 'end_time', 'result_url', 'result', 'failure_reason')

