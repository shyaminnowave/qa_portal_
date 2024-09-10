from rest_framework.views import APIView, Response
from apps.stb_tester.models import StbResult
from apps.stb_tester.utlity import StbAPI
from apps.testcases.models import TestCaseModel, AutomationChoices
from django.db import transaction
from rest_framework import status
from analytiqa.helpers.renders import ResponseInfo
from django.shortcuts import get_object_or_404


class STBResultGetView(APIView):
    
    def __init__(self, *args, **kwargs):
        self.response_format = ResponseInfo().response
        super(STBResultGetView, self).__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        stb = StbAPI()
        queryset = TestCaseModel.objects.filter(automation_status=AutomationChoices.AUTOMATABLE)
        _result = []
        try:
            for i in queryset:
                __query = TestCaseModel.objects.get(test_name=i.test_name)
                __result_instance = StbResult.objects.filter(testcase=i).last()
                if __result_instance:
                    response = stb.get_result(testcase=i.test_name, date=__result_instance.get_datetime())
                else:
                    response = stb.get_result(i.test_name)
                if response is False:
                    return Response("change user token")
                if response is not None:
                    for j in response:
                        _data = {
                            "result_id": j['result_id'],
                            "result_url": j['result_url'],
                            "triage_url": j['triage_url'],
                            "job_uid": j['job_uid'],
                            "start_time": j['start_time'],
                            "end_time": j['end_time'],
                            "testcase": __query,
                            "result": j['result'],
                            "failure_reason": j['failure_reason']
                        }
                        _result.append(StbResult(**_data))
                    with transaction.atomic():
                        StbResult.objects.bulk_create(_result, ignore_conflicts=True)
        except Exception as e:
            self.response_format["status"] = False
            self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
            self.response_format["data"] = "Error"
            self.response_format["message"] = str(e)
            return Response(self.response_format)
        self.response_format["status"] = True
        self.response_format["status_code"] = status.HTTP_200_OK
        self.response_format["data"] = "Success"
        self.response_format["message"] = "TestCase Uploaded Successfully"
        return Response(self.response_format)


class DemoResultView(APIView):

    def get(self, request, *args, **kwargs):
        pass
