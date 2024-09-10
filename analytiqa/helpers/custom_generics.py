import json
from typing import Any
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from analytiqa.helpers.renders import ResponseInfo
from rest_framework import status
from rest_framework.views import Request, Response


class CustomCreateAPIView(mixins.CreateModelMixin, GenericAPIView):

    def __init__(self, **kwargs: Any) -> None:
        self.response_format = ResponseInfo().response
        super().__init__(**kwargs)

    def post(self, request, *args, **kwargs):
            response = super().create(request, *args, **kwargs)
            if response.status_code == status.HTTP_201_CREATED:
                self.response_format['status'] = True
                self.response_format['status_code'] = response.status_code
                self.response_format['data'] = response.data
                self.response_format['message'] = "User Creation Successfull"
                return Response(self.response_format, status=status.HTTP_201_CREATED)
            else:
                self.response_format['status'] = False
                self.response_format['status_code'] = response.status_code
                self.response_format['data'] = 'Error'
                self.response_format['message'] = "User Creation Failed"
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)


class CustomRetriveAPIVIew(mixins.RetrieveModelMixin, GenericAPIView): 

    def __init__(self, **kwargs: Any) -> None:
        self.response_format = ResponseInfo().response
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        try:
            response = super().get(request, *args, **kwargs)
            if response.data:
                self.response_format['status'] = True
                self.response_format['status_code'] = status.HTTP_200_OK
                self.response_format['data'] = response.data
                self.response_format['message'] = "Success"
                return Response(self.response_format, status=status.HTTP_200_OK)
            else:
                self.response_format['status'] = False
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format['message'] = response.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.response_format['status'] = False
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomDestroyAPIView(mixins.DestroyModelMixin, GenericAPIView):

    def __init__(self, **kwargs: Any) -> None:
        self.response_format = ResponseInfo().response
        super().__init__(**kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            response = self.destroy(request, *args, **kwargs)
            if response.status_code == status.HTTP_204_NO_CONTENT:
                self.response_format['status'] = True
                self.response_format['status_code'] = status.HTTP_200_OK
                self.response_format['data'] = "Deleted"
                self.response_format['message'] = "Success"
                return Response(self.response_format, status=status.HTTP_200_OK)
            else:
                self.response_format['status'] = False
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format['message'] = response.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.response_format['status'] = False
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomUpdateAPIView(mixins.UpdateModelMixin, GenericAPIView): 
    
    def __init__(self, **kwargs: Any) -> None:
        self.response_format = ResponseInfo().response
        super().__init__(**kwargs)

    def put(self, request, *args, **kwargs):
        try:
            response = self.update(request, *args, **kwargs)
            if response.data:
                self.response_format['status'] = True
                self.response_format['status_code'] = status.HTTP_200_OK
                self.response_format['data'] = response.data
                self.response_format['message'] = "Success"
                return Response(self.response_format, status=status.HTTP_200_OK)
            else:
                self.response_format['status'] = False
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format['message'] = response.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.response_format['status'] = False
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def patch(self, request, *args, **kwargs):
        try:
            response = self.partial_update(request, *args, **kwargs)
            if response.data:
                self.response_format['status'] = True
                self.response_format['status_code'] = status.HTTP_200_OK
                self.response_format['data'] = response.data
                self.response_format['message'] = "Success"
                return Response(self.response_format, status=status.HTTP_200_OK)
            else:
                self.response_format['status'] = False
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format['message'] = response.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.response_format['status'] = False
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class CustomRetrieveUpdateAPIView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    
    def __init__(self, **kwargs: Any) -> None:
        self.response_format = ResponseInfo().response
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        try:
            response = super().retrieve(request, *args, **kwargs)
            if response.data:
                self.response_format['status'] = True
                self.response_format['status_code'] = status.HTTP_200_OK
                self.response_format['data'] = response.data
                self.response_format['message'] = "Success"
                return Response(self.response_format, status=status.HTTP_200_OK)
            else:
                self.response_format['status'] = False
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format['message'] = response.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.response_format['status'] = False
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, *args, **kwargs):
        try:
            response = self.update(request, *args, **kwargs)
            if response.data:
                self.response_format['status'] = True
                self.response_format['status_code'] = status.HTTP_200_OK
                self.response_format['data'] = response.data
                self.response_format['message'] = "Success"
                return Response(self.response_format, status=status.HTTP_200_OK)
            else:
                self.response_format['status'] = False
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format['message'] = response.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.response_format['status'] = False
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def patch(self, request, *args, **kwargs):
        try:
            response = self.partial_update(request, *args, **kwargs)
            if response.data:
                self.response_format['status'] = True
                self.response_format['status_code'] = status.HTTP_200_OK
                self.response_format['data'] = response.data
                self.response_format['message'] = "Success"
                return Response(self.response_format, status=status.HTTP_200_OK)
            else:
                self.response_format['status'] = False
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format['message'] = response.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.response_format['status'] = False
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomRetrieveDestroyAPIView(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    
    def __init__(self, **kwargs: Any) -> None:
        self.response_format = ResponseInfo().response
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        try:
            response = super().retrieve(request, *args, **kwargs)
            if response.data:
                self.response_format['status'] = True
                self.response_format['status_code'] = status.HTTP_200_OK
                self.response_format['data'] = response.data
                self.response_format['message'] = "Success"
                return Response(self.response_format, status=status.HTTP_200_OK)
            else:
                self.response_format['status'] = False
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format['message'] = response.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.response_format['status'] = False
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, *args, **kwargs):
        try:
            response = self.destroy(request, *args, **kwargs)
            if response.status_code == status.HTTP_204_NO_CONTENT:
                self.response_format['status'] = True
                self.response_format['status_code'] = status.HTTP_200_OK
                self.response_format['data'] = "Deleted"
                self.response_format['message'] = "Success"
                return Response(self.response_format, status=status.HTTP_200_OK)
            else:
                self.response_format['status'] = False
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format['message'] = response.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.response_format['status'] = False
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomRetrieveUpdateDestroyAPIView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                                         GenericAPIView):
    
    def __init__(self, **kwargs: Any) -> None:
        self.response_format = ResponseInfo().response
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        try:
            response = super().retrieve(request, *args, **kwargs)
            if response.data:
                self.response_format['status'] = True
                self.response_format['status_code'] = status.HTTP_200_OK
                self.response_format['data'] = response.data
                self.response_format['message'] = "Success"
                return Response(self.response_format, status=status.HTTP_200_OK)
            else:
                self.response_format['status'] = False
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format['message'] = response.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.response_format['status'] = False
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        try:
            response = self.update(request, *args, **kwargs)
            if response.data:
                self.response_format['status'] = True
                self.response_format['status_code'] = status.HTTP_200_OK
                self.response_format['data'] = response.data
                self.response_format['message'] = "Success"
                return Response(self.response_format, status=status.HTTP_200_OK)
            else:
                self.response_format['status'] = False
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format['message'] = response.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.response_format['status'] = False
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, *args, **kwargs):
        try:
            response = self.partial_update(request, *args, **kwargs)
            if response.data:
                self.response_format['status'] = True
                self.response_format['status_code'] = status.HTTP_200_OK
                self.response_format['data'] = response.data
                self.response_format['message'] = "Success"
                return Response(self.response_format, status=status.HTTP_200_OK)
            else:
                self.response_format['status'] = False
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format['message'] = response.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.response_format['status'] = False
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, *args, **kwargs):
        try:
            response = self.destroy(request, *args, **kwargs)
            if response.status_code == status.HTTP_204_NO_CONTENT:
                self.response_format['status'] = True
                self.response_format['status_code'] = status.HTTP_200_OK
                self.response_format['data'] = "Deleted"
                self.response_format['message'] = "Success"
                return Response(self.response_format, status=status.HTTP_200_OK)
            else:
                self.response_format['status'] = False
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format['message'] = response.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.response_format['status'] = False
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        