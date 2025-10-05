from functools import wraps

from django.http import HttpResponse

from django_htmx_tools.utils import is_htmx


def htmx_only_request(view_func):
    """
    Decorator that checks if a request is HTMX
    :param view_func:
    :return:
    """

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not is_htmx(request):
            return HttpResponse("Request must be made with HTMX", status=403)
        return view_func(request, *args, **kwargs)

    return wrapper
