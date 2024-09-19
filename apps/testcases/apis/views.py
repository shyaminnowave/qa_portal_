from rest_framework import generics
from collections import defaultdict
from apps.testcases.models import (
    TestCaseModel,
    TestCaseStep,
    NatcoStatus,
    TestcaseExcelResult,
    TestCaseChoices,
    AutomationChoices,
    StatusChoices,
    PriorityChoice,
    TestReport, Comment, ScriptIssue
)
from apps.testcases.apis.serializers import (
    TestCaseSerializerList,
    TestCaseSerializer,
    ExcelSerializer,
    NatcoStatusSerializer,
    DistinctTestResultSerializer,
    NavbarFilterSerializer,
    TestResultDRPSerializer,
    BulkFieldUpdateSerializer,
    NatcoGraphAPISerializer,
    GraphReportSerializer,
    TestStepSerializer,
    HistorySerializer,
    ScriptIssueSerializer,
    CommentSerializer
)
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from apps.testcases.pagination import CustomPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiSchemaBase
from drf_spectacular.openapi import OpenApiTypes, OpenApiExample
from django_filters import rest_framework as filters
from apps.testcases.filters import NatcoStatusFilter
from apps.stbs.permissions import AdminPermission
from analytiqa.helpers.renders import ResponseInfo
from analytiqa.helpers import custom_generics as cgenerics
from django.db.models import OuterRef, Subquery
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Min, F, Count, Subquery, OuterRef, Avg, Q
from apps.stbs.models import Natco
from apps.testcases.utlity import ReportExcel
# from apps.stb_tester.views import BaseAPI


class ResponseTemplateApi:

    def __init__(self, instance):
        self.response_format = ResponseInfo().response
        self.instance = instance

    def response(self):
        if self.instance == True:
            self.response_format["status"] = True
            self.response_format["status"] = True
            self.response_format["status_code"] = status.HTTP_200_OK
            self.response_format["data"] = "Success"
            self.response_format["message"] = "Success"
            return self.response_format
        else:
            self.response_format["status"] = False
            self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
            self.response_format["message"] = "error"
            return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)


class BulkFieldUpdateView(generics.GenericAPIView):

    serializer_class = BulkFieldUpdateSerializer

    def patch(self, request, *args, **kwargs):
        kwargs_splitted = kwargs.get("path").split("/")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            match kwargs_splitted[0]:
                case "status":
                    instance = serializer.update_testcase_status(
                        serializer.validated_data
                    )
                case "automation-status":
                    instance = serializer.update_testcase_automation(
                        serializer.validated_data
                    )
                case "natco":
                    match kwargs_splitted[1]:
                        case "status":
                            instance = serializer.update_natco_status(
                                serializer.validated_data
                            )
                        case _:
                            instance = False
                case _:
                    instance = False
            response_template = ResponseTemplateApi(instance)
            return Response(
                response_template.response(),
                status=status.HTTP_200_OK if instance else status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                "status": False,
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid data",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class TestCaseListView(generics.ListAPIView):

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [AdminPermission]
    queryset = TestCaseModel.objects.only(
        "jira_id",
        "test_name",
        "priority",
        "testcase_type",
        "status",
        "automation_status",
    ).all()
    serializer_class = TestCaseSerializerList
    pagination_class = CustomPagination
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = (
        "jira_id",
        "test_name",
        "status",
        "priority",
        "automation_status",
    )

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)
        return response


class TestCaseView(cgenerics.CustomCreateAPIView):

    # permission_classes = [AdminPermission]
    serializer_class = TestCaseSerializer

    def post(self, request, *args, **kwargs):
        return super(TestCaseView, self).post(request, *args, **kwargs)


class TestCaseDetailView(cgenerics.CustomRetrieveUpdateDestroyAPIView):

    # permission_classes = [AdminPermission]
    lookup_field = "id"
    serializer_class = TestCaseSerializer

    def get_object(self):
        queryset = get_object_or_404(
            TestCaseModel.objects.prefetch_related("test_steps"),
            id=self.kwargs.get("id"),
        )
        # natco = queryset.annotate(natco_status=Subquery(NatcoStatus.objects.select_related('test_case', 'language',
        # 'device', 'natco', 'user').filter(test_case_id=self.kwargs.get('jira_id'))))
        return queryset

    def get(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        # queryset = NatcoStatus.objects.select_related(
        #     "test_case", "language", "device", "natco", "user"
        # ).filter(test_case_id=self.kwargs.get("jira_id"))
        # serializer = NatcoStatusSerializer(queryset, many=True)
        # response.data["natco_status"] = serializer.data
        return response
    
    def put(self, request, *args, **kwargs):
        return super(TestCaseDetailView, self).put(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return super(TestCaseDetailView, self).patch(request, *args, **kwargs)


class TestCaseStepView(cgenerics.CustomCreateAPIView, cgenerics.CustomUpdateAPIView):

    serializer_class = TestStepSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
            self.response_format['status'] = status.HTTP_201_CREATED
            self.response_format['data'] = serializer.data
            self.response_format['message'] = 'Success'
            return Response(self.response_format, status=status.HTTP_201_CREATED)
        self.response_format['status'] = status.HTTP_400_BAD_REQUEST
        self.response_format['data'] = 'Error'
        self.response_format['message'] = 'Error'
        return Response(self.response_format, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        testcase_instance = TestCaseStep.objects.get(id=request.data['id'])
        serializer = self.get_serializer(instance=testcase_instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.update(instance=testcase_instance, validated_data=serializer.validated_data)
            self.response_format['status'] = status.HTTP_201_CREATED
            self.response_format['data'] = serializer.data
            self.response_format['message'] = 'Success'
            return Response(self.response_format, status=status.HTTP_201_CREATED)
        self.response_format['status'] = status.HTTP_400_BAD_REQUEST
        self.response_format['data'] = 'Error'
        self.response_format['message'] = 'Error'
        return Response(self.response_format, status=status.HTTP_201_CREATED)

    def delete(self, request):
        teststep_instance = TestCaseStep.objects.get(id=request.data.get('id'))
        serializer = self.get_serializer(instance=teststep_instance)
        serializer.delete()
        return Response({"success": True})


class TestStepDeleteView(cgenerics.CustomDestroyAPIView):

    serializer_class = TestStepSerializer

    def delete(self, request, *args, **kwargs):
        print(kwargs.get('id'))
        teststep_instance = TestCaseStep.objects.get(id=kwargs.get('id'))
        serializer = self.get_serializer(instance=teststep_instance)
        serializer.delete(teststep_instance)
        return Response("success")


class TestCaseNatcoView(generics.ListAPIView):

    # permission_classes = [AdminPermission]
    serializer_class = NatcoStatusSerializer
    queryset = NatcoStatus.objects.all()
    lookup_field = "id"
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = (
            NatcoStatus.objects.select_related("test_case", "natco_status")
            .filter(test_case_id=self.kwargs.get("jira_id"))
            .values("id", "summary")
        )
        return queryset


class TestCaseNatcoList(generics.ListAPIView):
    # permission_classes = [AdminPermission]
    serializer_class = NatcoStatusSerializer
    filterset_class = NatcoStatusFilter
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = NatcoStatus.objects.select_related(
            "test_case", "language", "device", "natco", "user"
        ).all()
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="Natco",
                description="Enter the Natco",
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="Language",
                description="Enter the Language",
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="Device",
                description="Enter the Device",
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="Jira Id",
                description="Enter the Jira ID",
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="Applicable",
                description="Enter the Applicable",
                required=False,
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="status",
                description="Choose a Status",
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                enum=NatcoStatus.NatcoStatusChoice.choices,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        data = self.get_queryset()
        filter_set = self.filterset_class(request.GET, self.get_queryset())
        if filter_set.is_valid():
            data = filter_set.qs
        paginated_data = self.paginate_queryset(data)
        serializer = self.get_serializer(paginated_data, many=True)
        try:
            if serializer:
                return self.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({"success": False, "data": "Error"})


class TestCaseNatcoDetail(cgenerics.CustomRetrieveUpdateDestroyAPIView):
    # permission_classes = [AdminPermission]
    serializer_class = NatcoStatusSerializer
    # queryset = NatcoStatus.objects.all()
    lookup_field = "pk"

    def get_object(self):
        queryset = NatcoStatus.objects.select_related("test_case").get(
            id=self.kwargs.get("pk")
        )
        return queryset


class FiltersView(APIView):

    def get(self, request, *args, **kwargs):
        testcase_status = [{"label": choice.label, "value": choice.value} for choice in TestCaseChoices]
        status = [{"label": choice.label, "value": choice.value} for choice in StatusChoices]
        priority = [{"label": choice.label, "value": choice.value} for choice in PriorityChoice]
        automation = [{"label": choice.label, "value": choice.value} for choice in AutomationChoices]
        _data = {
            "testcase_filter": testcase_status,
            "status": status,
            "priority": priority,
            "automation": automation
        }
        return Response(_data)


class TestResultFilterView(generics.GenericAPIView):

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super().__init__(**kwargs)

    serializer_class = TestResultDRPSerializer

    def get_queryset(self):
        queryset = TestcaseExcelResult.get_unique_filters()
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset:
            self.response_format["success"] = True
            self.response_format["status_code"] = status.HTTP_200_OK
            self.response_format["data"] = queryset
            self.response_format["message"] = "Success"
            return Response(self.response_format, status=status.HTTP_200_OK)
        if not queryset:
            self.response_format["success"] = False
            self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
            self.response_format["message"] = "Error"
            return Response(self.response_format, status=status.HTTP_200_OK)
        return Response(
            self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class NavBarFilter(generics.GenericAPIView):

    serializer_class = NavbarFilterSerializer

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super().__init__(**kwargs)

    def get_queryset(self):
        queryset = Natco.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        if serializer.data:
            self.response_format["success"] = True
            self.response_format["status_code"] = status.HTTP_200_OK
            self.response_format["data"] = serializer.data
            self.response_format["message"] = "Success"
            return Response(self.response_format, status=status.HTTP_200_OK)
        if not serializer.data:
            self.response_format["success"] = False
            self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
            self.response_format["message"] = "Error"
            return Response(self.response_format, status=status.HTTP_200_OK)
        return Response(
            self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class TestCaseDetailReport(generics.GenericAPIView):

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super().__init__(**kwargs)

    serializer_class = NatcoGraphAPISerializer

    def get_queryset(self):
        queryset = TestcaseExcelResult.objects.filter(
            testcase=self.request.GET.get("testcase")
        ).values("natco")
        natco = self.request.GET.get("natco")
        match self.kwargs.get("type"):
            case "load_time":
                if natco is not None:
                    queryset = queryset.filter(
                        natco__contains=self.request.GET.get("natco")
                    )
                queryset = queryset.annotate(avg_load_time=Avg("load_time"))
            case "cpu_load":
                if natco is not None:
                    queryset = queryset.filter(
                        natco__contains=self.request.GET.get("natco")
                    )
                queryset = queryset.annotate(avg_load_time=Avg("load_time"))
            case "ram_load":
                if natco is not None:
                    queryset = queryset.filter(
                        natco__contains=self.request.GET.get("natco")
                    )
                queryset = queryset.annotate(avg_load_time=Avg("load_time"))
            case _:
                raise ValueError
        return queryset

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        if serializer.data:
            self.response_format["success"] = True
            self.response_format["status_code"] = status.HTTP_200_OK
            self.response_format["data"] = serializer.data
            self.response_format["message"] = "Success"
            return Response(self.response_format, status=status.HTTP_200_OK)
        if not serializer.data:
            self.response_format["success"] = False
            self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
            self.response_format["message"] = "Error"
            return Response(self.response_format, status=status.HTTP_200_OK)
        return Response(
            self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class TestCaseReportView(generics.GenericAPIView):

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super().__init__(**kwargs)

    serializer_class = DistinctTestResultSerializer

    def get_queryset(self):
        results = TestcaseExcelResult.objects.values("testcase", "natco").annotate(
            min_cpu=Min("cpu_usage"),
            min_ram=Min("ram_usage"),
            min_time=Min("load_time"),
        )
        # Now, let's filter the results to get the distinct testcase and distinct natco with the minimum values
        distinct_results = []
        for result in results:
            distinct_result = TestcaseExcelResult.objects.filter(
                testcase=result["testcase"],
                natco=result["natco"],
                cpu_usage=result["min_cpu"],
                ram_usage=result["min_ram"],
                load_time=result["min_time"],
            ).first()
            if distinct_result:
                distinct_results.append(distinct_result)
        return distinct_results

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        if serializer.data:
            self.response_format["success"] = True
            self.response_format["status_code"] = status.HTTP_200_OK
            self.response_format["data"] = serializer.data
            self.response_format["message"] = "Success"
            return Response(self.response_format, status=status.HTTP_200_OK)
        if not serializer.data:
            self.response_format["success"] = False
            self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
            self.response_format["message"] = "Error"
            return Response(self.response_format, status=status.HTTP_200_OK)
        return Response(
            self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class ReportView(generics.GenericAPIView):

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super().__init__(**kwargs)

    serializer_class = GraphReportSerializer

    def get_queryset(self):
        queryset = TestReport.objects.values('testcase__test_name', 'node').annotate(
                                                                              cpu=Min("cpu_usage_percentile"),
                                                                              loadtime=Min("loadtime_percentile"),
                                                                              ram=Min("ram_usage_percentile")
                                                                            )
        return queryset

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        _data = defaultdict(lambda: defaultdict(list))
        for item in serializer.data:
            cpu_data = {
                'natco': item['natco'],
                'buildname': item['natco_version'],
                'value': item['cpu']
            }
            ram_data = {
                'natco': item['natco'],
                'buildname': item['natco_version'],
                'value': item['ram']
            }
            load_data = {
                'natco': item['natco'],
                'buildname': item['natco_version'],
                'value': item['loadtime']
            }
            _data[item['testcase']]['cpu'].append(cpu_data)
            _data[item['testcase']]['ram'].append(ram_data)
            _data[item['testcase']]['loadtime'].append(load_data)
        final_output = []
        for testcase_name, metrics in _data.items():
            final_output.append({
                'testcaseName': testcase_name,
                'cpu': metrics['cpu'],
                'RAM': metrics['ram'],
                'Load': metrics['loadtime']
            })
        if final_output:
            self.response_format["success"] = True
            self.response_format["status_code"] = status.HTTP_200_OK
            self.response_format["data"] = final_output
            self.response_format["message"] = "Success"
            return Response(self.response_format, status=status.HTTP_200_OK)
        if not final_output:
            self.response_format["success"] = False
            self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
            self.response_format["message"] = "Error"
            return Response(self.response_format, status=status.HTTP_200_OK)
        return Response(
            self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class TestReportGraphView(generics.GenericAPIView):

    def get_queryset(self):
        queryset = TestReport.objects.values('testcase__test_name', 'node').annotate(
                                                                              cpu=Min("cpu_usage_percentile"),
                                                                              loadtime=Min("loadtime_percentile"),
                                                                              ram=Min("ram_usage_percentile")
                                                                            )
        return queryset


class TestView(APIView):

    def __init__(self, **kwargs) -> None:
        self.response_format = ResponseInfo().response
        super().__init__(**kwargs)

    def get_query_dict(self):
        _dict = {}
        testcase = TestcaseExcelResult.objects.distinct("testcase", "natco")
        for t in testcase:
            try:
                test = TestcaseExcelResult.objects.filter(testcase=t)
                for i in test:
                    if i.testcase not in _dict:
                        _dict[t.testcase] = {
                            i.natco: {
                                "load_time": i.load_time,
                                "cpu_usage": i.cpu_usage,
                                "ram_usage": i.ram_usage,
                            }
                        }
                    else:
                        x = _dict[t.testcase]
                        x[i.natco] = {
                            "load_time": i.load_time,
                            "cpu_usage": i.cpu_usage,
                            "ram_usage": i.ram_usage,
                        }
            except TestcaseExcelResult.DoesNotExist:
                _dict[t] = False
        return _dict

    def get(self, request, *args, **kwargs):
        queryset = self.get_query_dict()
        if queryset:
            self.response_format["status"] = True
            self.response_format["status_code"] = status.HTTP_200_OK
            self.response_format["data"] = queryset
            self.response_format["message"] = "Success"
        else:
            self.response_format["status"] = False
            self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
            self.response_format["message"] = "No Data"
        return Response(self.response_format)


class ExcelUploadView(generics.GenericAPIView):

    serializer_class = ExcelSerializer

    def post(self, request, *args, **kwargs):
        try:
            kwargs_splitted = kwargs.get("path").split("/")
            method = request.FILES.get("file")
            print("method", method)
            instance = None
            if kwargs_splitted[0] == "report":
                instance = ReportExcel(file=method).import_data()
            return Response(instance)
        except Exception as e:
            return Response(str(e))


class DemoView(generics.GenericAPIView):

    serializer_class = TestCaseSerializer

    def get_queryset(self):
        queryset = TestCaseModel.objects.prefetch_related('test_steps').get(id=13005)
        print(len(queryset.test_steps.all()))
        return queryset

    def get(self, request):
        serializer = self.get_serializer(self.get_queryset())
        return Response(serializer.data)


class DemoHistoryView(generics.GenericAPIView):

    serializer_class = HistorySerializer

    def get_queryset(self):
        queryset = TestCaseModel.objects.get(id=13000)
        return queryset.history.all()

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class ScriptIssueView(generics.ListCreateAPIView):

    def __init__(self, **kwargs) -> None:
        self.response_format = ResponseInfo().response
        super().__init__(**kwargs)

    serializer_class = ScriptIssueSerializer

    def get_queryset(self):
        queryset = TestCaseModel.objects.prefetch_related('issues').get(id=self.kwargs.get("id"))
        return queryset.issues.all()

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        if serializer.data:
            self.response_format["status"] = True
            self.response_format["status_code"] = status.HTTP_200_OK
            self.response_format["data"] = serializer.data
            self.response_format["message"] = "Success"
        else:
            self.response_format["status"] = False
            self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
            self.response_format["message"] = "No Data"
        return Response(self.response_format)


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.create(serializer.validated_data, id=self.kwargs.get('id', None))
                self.response_format["status"] = True
                self.response_format["status_code"] = status.HTTP_200_OK
                self.response_format["data"] = serializer.data
                self.response_format["message"] = "Success"
                return Response(self.response_format)
            self.response_format["status"] = False
            self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
            self.response_format["message"] = serializer.errors
            return Response(self.response_format)
        except Exception as e:
            self.response_format["status"] = False
            self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
            self.response_format["message"] = str(e)
            return Response(self.response_format)


class ScriptIssueDetailView(generics.GenericAPIView):

    def __init__(self, **kwargs) -> None:
        self.response_format = ResponseInfo().response
        super().__init__(**kwargs)


    serializer_class = ScriptIssueSerializer

    def get_queryset(self):
        queryset = ScriptIssue.objects.get(id=self.kwargs.get("id"))
        return queryset

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset())
        if serializer.data:
            self.response_format["status"] = True
            self.response_format["status_code"] = status.HTTP_200_OK
            self.response_format["data"] = serializer.data
            self.response_format["message"] = "Success"
        else:
            self.response_format["status"] = False
            self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
            self.response_format["message"] = "No Data"
        return Response(self.response_format)

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.get_queryset(), data=request.data)
        if serializer.is_valid():
            serializer.save()
            self.response_format["status"] = True
            self.response_format["status_code"] = status.HTTP_200_OK
            self.response_format["data"] = serializer.data
            self.response_format["message"] = "Success"
            return Response(self.response_format)
        self.response_format["status"] = False
        self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
        self.response_format["message"] = "No Data"
        return Response(self.response_format)



class CommentsView(generics.ListCreateAPIView):

    def __init__(self, **kwargs) -> None:
        self.response_format = ResponseInfo().response
        super().__init__(**kwargs)

    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.filter(object_id=self.kwargs['id'])
        return queryset

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        if serializer:
            self.response_format["status"] = True
            self.response_format["status_code"] = status.HTTP_200_OK
            self.response_format["data"] = serializer.data
            self.response_format["message"] = "Success"
        else:
            self.response_format["status"] = False
            self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
            self.response_format["message"] = "No Data"
        return Response(self.response_format)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            self.response_format["status"] = True
            self.response_format["status_code"] = status.HTTP_200_OK
            self.response_format["data"] = serializer.data
            self.response_format["message"] = "Success"
            return Response(self.response_format)
        self.response_format["status"] = False
        self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
        self.response_format["message"] = "No Data"
        return Response(self.response_format)



class CommentEditView(generics.GenericAPIView):

    def __init__(self, **kwargs) -> None:
        self.response_format = ResponseInfo().response
        super().__init__(**kwargs)

    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.get(id=self.kwargs['pk'])
        return queryset

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset())
        if serializer:
            self.response_format["status"] = True
            self.response_format["status_code"] = status.HTTP_200_OK
            self.response_format["data"] = serializer.data
            self.response_format["message"] = "Success"
        else:
            self.response_format["status"] = False
            self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
            self.response_format["message"] = "No Data"
        return Response(self.response_format)

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.get_queryset(), data=request.data)
        if serializer.is_valid():
            serializer.save()
            self.response_format["status"] = True
            self.response_format["status_code"] = status.HTTP_200_OK
            self.response_format["data"] = serializer.data
            self.response_format["message"] = "Success"
            return Response(self.response_format)
        self.response_format["status"] = False
        self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
        self.response_format["message"] = "No Data"
        return Response(self.response_format)