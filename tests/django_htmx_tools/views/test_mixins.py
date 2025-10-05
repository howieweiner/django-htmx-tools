import pytest
from django.http import HttpResponse
from django.test import RequestFactory
from django.views.generic import TemplateView

from django_htmx_tools.views.mixins import IsHtmxRequestMixin


def setup_view_for_testing(view_class, request, **view_kwargs):
    """
    Helper function to properly set up a view for testing.
    This mimics what Django does during request processing.
    """
    view = view_class()
    view.setup(request, **view_kwargs)
    view.request = request
    return view


@pytest.fixture
def request_factory():
    """Create a RequestFactory instance"""
    return RequestFactory()


@pytest.fixture
def htmx_request(request_factory):
    """Create an HTMX request"""
    request = request_factory.post(
        "/test/",
        HTTP_HX_REQUEST="true",
        HTTP_HX_TRIGGER_NAME="test_field",
    )
    return request


@pytest.fixture
def non_htmx_request(request_factory):
    """Create a non-HTMX request"""
    request = request_factory.post("/test/")
    return request


def test_allows_htmx_request(htmx_request):
    """Should allow HTMX requests"""

    class MockView(IsHtmxRequestMixin, TemplateView):
        template_name = "test.html"

        def post(self, request, *args, **kwargs):
            return HttpResponse("Success")

    view = setup_view_for_testing(MockView, htmx_request)
    response = view.dispatch(htmx_request)

    assert response.status_code == 200
    assert response.content == b"Success"


def test_prevents_non_htmx_request(non_htmx_request):
    """Should prevent non-HTMX requests with 403"""

    class MockView(IsHtmxRequestMixin, TemplateView):
        template_name = "test.html"

        def get(self, request, *args, **kwargs):
            return HttpResponse("Success")

    view = MockView()
    response = view.dispatch(non_htmx_request)

    assert response.status_code == 403
    assert b"Request must be made with HTMX" in response.content  # type: ignore[attr-defined]
