from typing import Any
from rest_framework.views import Response
from rest_framework import generics
from apps.account.models import Account
from apps.account.apis.serializers import AccountSerializer, LoginSerializer, ProfileSerializer, UserListSerializer, \
                                PermissionSerializer, GroupListSerializer, GroupSerializer, UserSerializer
from django.contrib.auth import authenticate
from rest_framework import status
from apps.account.utils import get_token_for_user
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.account.signals import user_token_login, user_token_logout
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, extend_schema_view
from drf_spectacular.types import OpenApiTypes
from apps.testcases.apis.views import CustomPagination
from django.contrib.auth.models import Group, Permission
from apps.account.permissions import AdminUserPermission, DjangoModelPermissions, UserPermission, \
    GroupCreatePermission, DjangoObjectPermissions
from rest_framework.permissions import IsAuthenticated
from analytiqa.helpers.renders import ResponseInfo
from analytiqa.helpers import custom_generics as cgenerics


# ------------------------------ ListAPIS ------------------------------

class PermissionListView(generics.ListAPIView):

    # permission_classes = [AdminUserPermission]
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class GroupView(generics.ListAPIView):

    # permission_classes = [UserPermission]
    queryset = Group.objects.all()
    serializer_class = GroupListSerializer

    def get_serializer_context(self):
        return {"request": self.request}


class UserListView(generics.ListAPIView):

    # permission_classes = [UserPermission]

    queryset = Account.objects.all()
    serializer_class = UserListSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Account.objects.only('fullname', 'username', 'email', 'groups').prefetch_related('groups').all()
        return queryset


# ------------------------------ APIViews ------------------------------

class LogoutView(APIView):

    def __init__(self, **kwargs: Any) -> None:
        self.response_format = ResponseInfo().response
        super().__init__(**kwargs)

    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            if request.user.is_authenticated and isinstance(request.user, Account):
                user_token_logout.send(sender=request.user.__class__, user=request.user, request=request)
                token.blacklist()
                self.response_format['status'] = True
                self.response_format['status_code'] = status.HTTP_200_OK
                self.response_format['message'] = "User Logout Successfull"
                return Response(self.response_format,
                                        status=status.HTTP_200_OK)
        except Exception as e:
            self.response_format['status'] = False
            self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
            self.response_format['message'] = str(e)
            return Response(self.response_format,
                status=status.HTTP_404_NOT_FOUND)


# ------------------------------ Generic APIS ------------------------------

class LoginView(generics.GenericAPIView):

    def __init__(self, **kwargs: Any) -> None:
        self.response_format = ResponseInfo().response
        super().__init__(**kwargs)

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                self.response_format['status'] = False
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format['message'] = "Please Enter the Correct Details"
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

            user_cred = self._perform_login(request, email=serializer.validated_data.get('email', None),
                                            password=serializer.validated_data.get('password', None))

            if user_cred is not None:
                self.response_format['status'] = True
                self.response_format['status_code'] = status.HTTP_200_OK
                self.response_format['data'] = user_cred
                self.response_format['message'] = "User Login Successfull"
                response = Response(self.response_format,
                                    status=status.HTTP_200_OK)
                return response
            else:
                self.response_format['status'] = False
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format['data'] = user_cred
                self.response_format['message'] = "User Login Successfull"
                return Response(self.response_format,
                                status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            self.response_format['status'] = False
            self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
            self.response_format['message'] = str(e)
            return Response({'success': False, 'error': "Please Check the login Creditionals"},
                            status=status.HTTP_404_NOT_FOUND)

    def _perform_login(self, request, email, password):
        user = authenticate(email=email, password=password)
        if user is not None:
            user_token_login.send(sender=user, user=user, request=request)
            token = get_token_for_user(user)
            return {
                'access': token['access'],
                'refresh': token['refresh'],
                'email': user.email,
                'username': user.username
            }
        return None


class UserProfileView(generics.GenericAPIView):

    def __init__(self, **kwargs: Any) -> None:
        self.response_format = ResponseInfo().response
        super().__init__(**kwargs)

    # permission_classes = [UserPermission]
    serializer_class = ProfileSerializer
    lookup_field = 'username'

    def get_object(self):
        queryset = Account.objects.only('fullname', 'email', 'groups').select_related('groups').get(username=self.kwargs.get('username'))
        return queryset

    def get(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(self.get_object())
            if serializer.data:
                self.response_format['status'] = True
                self.response_format['status_code'] = status.HTTP_200_OK
                self.response_format['data'] = serializer.data
                self.response_format['message'] = "Success"
                return Response(self.response_format)
            else:
                self.response_format['status'] = False
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format['message'] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.response_format['status'] = False
            self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        """ Pending """
        pass


# ------------------------------ CustomGeneric APIS ------------------------------


class AccountCreateView(cgenerics.CustomCreateAPIView):

    serializer_class = AccountSerializer


class UserUpdateGroup(cgenerics.CustomRetrieveUpdateAPIView):

    # permission_classes = [AdminUserPermission]

    queryset = Account.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


class GroupCreateView(cgenerics.CustomCreateAPIView):

    # permission_classes = [DjangoModelPermissions]

    queryset = Group.objects.all()
    serializer_class = GroupListSerializer

    def post(self, request, *args, **kwargs):
        response = super(GroupCreateView, self).post(request, *args, **kwargs)
        return Response({'success': True, 'data': response.data})


class GroupDetailView(cgenerics.CustomRetrieveUpdateAPIView):
    # permission_classes = [DjangoObjectPermissions]

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    lookup_field = 'pk'


class GroupUsers(cgenerics.CustomRetriveAPIVIew):

    def get_queryset(self):
        queryset = Group.objects.select_related('groups').all()
        return queryset

    serializer_class = ProfileSerializer

