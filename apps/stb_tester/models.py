import datetime
from django.db import models
from solo.models import SingletonModel
from django_extensions.db.models import TimeStampedModel
from apps.testcases.models import TestCaseModel
from django.utils.translation import gettext_lazy as _

# Create your models here.


class StbConfiguration(SingletonModel):
    access_token = models.CharField(max_length=50)
    base_endpoint = models.URLField(max_length=100)

    def __str__(self):
        return self.access_token

    def get_access_token(self):
        return self.access_token


class StbResult(TimeStampedModel):

    class ResultChoice(models.TextChoices):
        PASS = 'pass', _('Pass')
        FAIL = 'fail', _('Fail')
        ERROR = 'error', _('Error')

    result_id = models.CharField(max_length=255)
    job_uid = models.CharField(max_length=255)
    result_url = models.URLField()
    triage_url = models.URLField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    testcase = models.ForeignKey(TestCaseModel, on_delete=models.CASCADE, related_name='testcase_result')
    result = models.CharField(choices=ResultChoice.choices, max_length=10)
    failure_reason = models.TextField(default='', blank=True, null=True)

    def __str__(self):
        return self.result_id

    def get_result(self):
        return self.result[:20]

    def get_datetime(self):
        _start_time = str(self.start_time).split(' ')
        _remove_gmt = _start_time[-1].split('+')
        if _remove_gmt and _start_time:
            _remove_gmt.pop()
            _start_time.pop()
        _start_time.extend(_remove_gmt)
        return 'T'.join(_start_time)


