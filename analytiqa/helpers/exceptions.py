from rest_framework.exceptions import APIException, ValidationError, ReturnDict, ReturnList, force_str, ErrorDetail
from rest_framework import status
from django.utils.translation import gettext_lazy as _


def _get_error_details(data, default_code=None):
    """
    Descend into a nested data structure, forcing any
    lazy translation strings or strings into `ErrorDetail`.
    """
    if isinstance(data, (list, tuple)):
        ret = [
            _get_error_details(item, default_code) for item in data
        ]
        if isinstance(data, ReturnList):
            return ReturnList(ret, serializer=data.serializer)
        return ret
    elif isinstance(data, dict):
        ret = {
            key: _get_error_details(value, default_code)
            for key, value in data.items()
        }
        if isinstance(data, ReturnDict):
            return ReturnDict(ret, serializer=data.serializer)
        return ret

    text = force_str(data)
    code = getattr(data, 'code', default_code)
    return ErrorDetail(text, code)


class CustomFieldException(APIException):

    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = 'Invalid Data'
    default_code = 'invalid'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        if isinstance(detail, tuple):
            detail = list(detail)
        elif not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]
        self.detail = _get_error_details(detail, code)

    
class TokenExpireException(APIException):

    status = status.HTTP_403_FORBIDDEN
    default_detail = _('Stb Token Expired')
    default_code = 'authentication_failed'
