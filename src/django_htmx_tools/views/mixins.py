from django.http import HttpResponse

from django_htmx_tools.utils import is_htmx


class IsHtmxRequestMixin:
    """
    Mixin to check if a request is HTMX
    """
    def dispatch(self, request, *args, **kwargs):
        if not is_htmx(request):
            return HttpResponse("Request must be made with HTMX", status=403)
        return super(IsHtmxRequestMixin, self).dispatch(request, *args, **kwargs)
