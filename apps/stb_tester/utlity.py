import requests
from abc import ABCMeta
from rest_framework.views import Response
from ..stb_tester.models import StbConfiguration, StbResult
from rest_framework.views import APIView
from apps.testcases.models import TestCaseModel


class BaseAPI(metaclass=ABCMeta):

    def get_base_url(self):
        pass

    def get_token(self):
        pass

    def get_result(self):
        pass

# -------------------------------------


class StbAPI(BaseAPI):

    def get_base_url(self):
        url = StbConfiguration.objects.get()
        return url.base_endpoint

    @property
    def get_token(self):
        token = StbConfiguration.objects.get()
        return token.access_token

    def add_date_filter(self, testcase, date):
        url = '%sresults?filter=testcase:%s+date:>"%s"&sort=date:asc' % (self.get_base_url(), testcase, date)
        return url

    def add_testcase_filter(self, testcase, date):
        url = '%sresults?filter=testcase:%s&sort=date:asc' % (self.get_base_url(), testcase)
        return url

    def get_result(self, testcase=None, date=None):
        result_url = None
        if date:
            result_url = self.add_date_filter(testcase, date)
        else:
            result_url = self.add_testcase_filter(testcase, date)
        response = requests.get(url=result_url, headers={"Authorization": f"token {self.get_token}"})
        if response.status_code in [403, 400, 404, 500]:
            return False
        elif response.status_code == 200:
            return response.json()
        return False


