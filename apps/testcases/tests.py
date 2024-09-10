import pytest
from django.test import TestCase
from apps.testcases.models import TestCaseModel, NatcoStatus
from apps.stbs.models import STBManufacture, Language, Natco, NactoManufactureLanguage
from rest_framework.test import APIClient
from django.urls import reverse
from apps.testcases.models import NatcoStatus
from rest_framework import status
# Create your tests here.


@pytest.mark.django_db
class TestTestCaseModel:

    def test_create_test_case(self):
        test_case = TestCaseModel.objects.create(
            jira_id=1,
            test_name="Test Case 1",
            jira_summary="Summary",
            test_description="Description",
            status=TestCaseModel.ONGOING,
            automation_status=TestCaseModel.IN_DEVELOPMENT,
            script_name="TestScript",
            script="ScriptContent"
        )

        assert test_case.jira_id == 1
        assert test_case.test_name == "Test Case 1"
        assert test_case.jira_summary == "Summary"
        assert test_case.test_description == "Description"
        assert test_case.status == TestCaseModel.ONGOING
        assert test_case.automation_status == TestCaseModel.IN_DEVELOPMENT
        assert test_case.script_name == "TestScript"
        assert test_case.script == "ScriptContent"

    def test_default_values(self):
        test_case = TestCaseModel.objects.create(
            jira_id=2,
            test_name="Test Case 2",
            jira_summary="Summary 2",
            test_description="Description 2",
            automation_status=TestCaseModel.NOT_AUTOMATABLE
        )
        assert test_case.status == TestCaseModel.ONGOING  # default value
        assert not test_case.script_name  # default value
        assert not test_case.script  # default value


@pytest.mark.django_db
class TestNatcoList:

    def setup_method(self):
        self.client = APIClient()
        natoc = Natco.objects.create(country='Poland', natco='PL')
        device = STBManufacture.objects.create(name="SDMC")
        language = Language.objects.create(language_name="English")
        _data = NactoManufactureLanguage.objects.create(natco=natoc, device_name=device,
                                                        language_name=language)
        self.test_case = TestCaseModel.objects.create(
            jira_id=1,
            test_name="Test Case 1",
            jira_summary="Summary",
            test_description="Description",
            status=TestCaseModel.ONGOING,
            automation_status=TestCaseModel.IN_DEVELOPMENT,
            script_name="TestScript",
            script="ScriptContent"
        )

    def test_view_data(self):

        self._url = reverse('testcase-natco', kwargs={'jira_id': self.test_case.jira_id})
        self.response = self.client.get(self._url)
        response_data = self.response.json()
        assert response_data['count'] == 1


@pytest.mark.django_db
class TestNatcoStatus:

    def setup_method(self):
        self.client = APIClient()
        natoc = Natco.objects.create(country='Poland', natco='PL')
        device = STBManufacture.objects.create(name="SDMC")
        language = Language.objects.create(language_name="English")
        _data = NactoManufactureLanguage.objects.create(natco=natoc, device_name=device,
                                                        language_name=language)
        self.test_case = TestCaseModel.objects.create(
            jira_id=1,
            test_name="Test Case 1",
            jira_summary="Summary",
            test_description="Description",
            status=TestCaseModel.ONGOING,
            automation_status=TestCaseModel.IN_DEVELOPMENT,
            script_name="TestScript",
            script="ScriptContent"
        )
        self._url = reverse('natco-list')

    def test_view_data(self):
        self._url = reverse('natco-list')
        self.response = self.client.get(self._url)
        response_data = self.response.json()
        assert response_data['count'] == 1

    def test_natco_status_update(self):
        _data = {
            "status": NatcoStatus.IN_DEVELOPMENT,
            "applicable": "False"
        }
        natco = NatcoStatus.objects.get(id=1)
        self._url = reverse('natco-details', kwargs={'pk': natco.id})
        self.response = self.client.patch(self._url, _data)
        self.testcase_instance = TestCaseModel.objects.get(jira_id=self.test_case.jira_id)
        response_data = self.response.json()
        assert self.testcase_instance.automation_status == 'in-development'
        assert response_data['success'] == True
        assert response_data['data']['status'] == "in_development"



