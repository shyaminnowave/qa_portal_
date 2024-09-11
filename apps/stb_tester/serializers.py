from idlelib.replace import replace
from django.utils.datetime_safe import datetime
from rest_framework import serializers
from apps.stb_tester.models import StbResult


class ResultSerializer(serializers.ModelSerializer):

    end_time = serializers.SerializerMethodField()
    start_time = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()

    class Meta:
        model = StbResult
        fields = ('start_time', 'end_time', 'duration', 'result_url', 'result', 'failure_reason')

    def get_start_time(self, obj):
        return obj.get_time('start_time')

    def get_end_time(self, obj):
        instance = datetime.strptime(obj.get_time('end_time'), "%Y-%m-%d %H:%M:%S.%f").replace(microsecond=0)
        instance = str(instance).replace('T', ' ')
        return instance

    def get_duration(self, obj):
        start = datetime.strptime(self.get_start_time(obj), "%Y-%m-%d %H:%M:%S").replace(microsecond=0)
        end = datetime.strptime(self.get_end_time(obj), "%Y-%m-%d %H:%M:%S").replace(microsecond=0)
        duration = end - start
        return duration.total_seconds()



