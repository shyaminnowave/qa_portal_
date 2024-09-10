from django.utils.deprecation import MiddlewareMixin


class ExceptionMiddelware(MiddlewareMixin):

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def process_response(self, request, response):
        if response.status_code == 403:
            response.data = {"detail": "Custom Forbidden Message"}
        return response

