from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)
    if isinstance(exc, (ValidationError, ValueError)):
        error_message = str(exc)
        return Response({'message': error_message}, status=status.HTTP_404_NOT_FOUND)
    return Response  