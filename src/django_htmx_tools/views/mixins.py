from typing import Any

from django.http import HttpRequest, HttpResponse

from django_htmx_tools.utils import is_htmx


class IsHtmxRequestMixin:
    """
    Mixin to check if a request is HTMX
    """

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not is_htmx(request):
            return HttpResponse("Request must be made with HTMX", status=403)
        return super().dispatch(request, *args, **kwargs)  # type: ignore[misc]
