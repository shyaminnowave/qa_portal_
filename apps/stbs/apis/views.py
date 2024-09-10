from typing import Any
from rest_framework import generics 
from rest_framework.viewsets import ModelViewSet
from apps.stbs.models import Language, STBManufacture, Natco, NactoManufactureLanguage
from apps.stbs.apis.serializers import LanguageSerializer, STBManufactureSerializer, NactoSerializer, \
    NatcoLanguageSerializer, NatcoOptionSerializer, LanguageOptionSerializer, DeviceOptionSerializer, \
    ReportFilterSerializer
from apps.testcases.pagination import CustomPagination
from apps.stbs.mixins import OptionMixin
from apps.stbs.permissions import LangaugeOptionPermission, NatcoOptionPermission, DeviceOptionPermission, \
        AdminPermission, LanguagePermission
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiSchemaBase
from drf_spectacular.openapi import OpenApiTypes, OpenApiExample
from analytiqa.helpers.renders import ResponseInfo
from rest_framework import status
from rest_framework.views import Response


class LanguageViewset(ModelViewSet):
    # permission_classes = [LanguagePermission]
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    pagination_class = CustomPagination

    @extend_schema(
        request=LanguageSerializer,
        responses={201, LanguageSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class STBManufactureViewSet(ModelViewSet):
    # permission_classes = [AdminPermission]
    queryset = STBManufacture.objects.all()
    serializer_class = STBManufactureSerializer
    pagination_class = CustomPagination


class NatcoViewSet(ModelViewSet):
    # permission_classes = [AdminPermission]
    queryset = Natco.objects.all()
    serializer_class = NactoSerializer
    pagination_class = CustomPagination


class NatcoLanguageViewSet(ModelViewSet):
    # permission_classes = [AdminPermission]
    queryset = NactoManufactureLanguage.objects.all()
    serializer_class = NatcoLanguageSerializer
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        return super(NatcoLanguageViewSet, self).create()


class NatcoOptionView(OptionMixin, generics.GenericAPIView):

    def __init__(self, **kwargs: Any) -> None:
        self.response_format = ResponseInfo().response
        super().__init__(**kwargs)

    # permission_classes = [NatcoOptionPermission]
    queryset = Natco.objects.all()
    serializer_class = NatcoOptionSerializer

    def get(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(self.get_queryset(), many=True)
            if serializer.data:
                self.response_format['status'] = True
                self.response_format['status_code'] = status.HTTP_200_OK
                self.response_format['data'] = serializer.data
                self.response_format['message'] = "Success"
                return Response(self.response_format, status=status.HTTP_200_OK)
            elif not serializer.data:
                self.response_format['status'] = True
                self.response_format['status_code'] = status.HTTP_404_NOT_FOUND
                self.response_format['message'] = "No Data"
                return Response(self.response_format, status=status.HTTP_200_OK)
        except Exception as e:
            self.response_format['status'] = True
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['message'] = "No Data"
            return Response(self.response_format, status=status.HTTP_200_OK)


class LanguageOptionView(OptionMixin, generics.GenericAPIView):

    def __init__(self, **kwargs: Any) -> None:
        self.response_format = ResponseInfo().response
        super().__init__(**kwargs)

    # permission_classes = [LangaugeOptionPermission]
    queryset = Language.objects.all()
    serializer_class = LanguageOptionSerializer

    def get(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(self.get_queryset(), many=True)
            if serializer.data:
                self.response_format['status'] = True
                self.response_format['status_code'] = status.HTTP_200_OK
                self.response_format['data'] = serializer.data
                self.response_format['message'] = "Success"
                return Response(self.response_format, status=status.HTTP_200_OK)
            elif not serializer.data:
                self.response_format['status'] = True
                self.response_format['status_code'] = status.HTTP_404_NOT_FOUND
                self.response_format['message'] = "No Data"
                return Response(self.response_format, status=status.HTTP_200_OK)
        except Exception as e:
            self.response_format['status'] = True
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['message'] = "No Data"
            return Response(self.response_format, status=status.HTTP_200_OK)


class DeviceOptionView(OptionMixin, generics.GenericAPIView):

    def __init__(self, **kwargs: Any) -> None:
        self.response_format = ResponseInfo().response
        super().__init__(**kwargs)

    # permission_classes = [DeviceOptionPermission]
    queryset = STBManufacture.objects.all()
    serializer_class = DeviceOptionSerializer

    def get(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(self.get_queryset(), many=True)
            if serializer.data:
                self.response_format['status'] = True
                self.response_format['status_code'] = status.HTTP_200_OK
                self.response_format['data'] = serializer.data
                self.response_format['message'] = "Success"
                return Response(self.response_format, status=status.HTTP_200_OK)
            elif not serializer.data:
                self.response_format['status'] = True
                self.response_format['status_code'] = status.HTTP_404_NOT_FOUND
                self.response_format['message'] = "No Data"
                return Response(self.response_format, status=status.HTTP_200_OK)
        except Exception as e:
            self.response_format['status'] = True
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_200_OK)


class ReportFilterView(generics.GenericAPIView):

    serializer_class = ReportFilterSerializer
    queryset = NactoManufactureLanguage.objects.filter(natco__natco='HU').\
                                                       exclude(language_name__language_name='English').\
                                                       values('device_name__name').annotate()

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)
