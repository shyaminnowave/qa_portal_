from celery import shared_task
from apps.stb_tester.models import StbTestCaseResult
from apps.stb_tester.views import StbAPI
from apps.testcases.models import TestCaseModel, AutomationChoices
from django.db import transaction


@shared_task()
def get_stb_result(stb=StbAPI()):
    queryset = TestCaseModel.objects.filter(automation_status=AutomationChoices.AUTOMATABLE)
    _result = []
    try:
        for i in queryset:
            response = stb.get_result(i.test_name)
            _to_python = response.json()
            for j in _to_python:
                _data = {
                    "result_id": j['result_id'],
                    "result_url": j['result_url'],
                    "triage_url": j['triage_url'],
                    "job_uid": j['job_uid'],
                    "start_time": j['start_time'],
                    "end_time": j['end_time'],
                    "test_case": j['test_case'],
                    "result": j['result'],
                    "failure_reason": j['failure_reason']
                }
                _result.append(StbTestCaseResult(_data))
        with transaction.atomic():
            TestCaseModel.objects.bulk_create(_result)
    except Exception as e:
        print(str(e))
        return str(e)




