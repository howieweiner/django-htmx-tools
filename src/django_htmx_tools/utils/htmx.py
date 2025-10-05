from django.http import HttpRequest


def is_htmx(request: HttpRequest):
    """
    Check if a request is HTMX
    :param request:
    :return: True if the request is HTMX, False otherwise
    """
    return request.headers.get("Hx-Request") == "true"
