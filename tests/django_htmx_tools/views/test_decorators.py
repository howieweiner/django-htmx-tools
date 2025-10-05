import pytest
from django.http import HttpResponse
from django.test import RequestFactory

from django_htmx_tools.views.decorators import htmx_only_request


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
    """Should allow HTMX requests and call the decorated view function"""

    @htmx_only_request
    def mock_view(request):
        return HttpResponse("Success")

    response = mock_view(htmx_request)

    assert response.status_code == 200
    assert response.content == b"Success"


def test_prevents_non_htmx_request(non_htmx_request):
    """Should prevent non-HTMX requests with 403 response"""

    @htmx_only_request
    def mock_view(request):
        return HttpResponse("Success")

    response = mock_view(non_htmx_request)

    assert response.status_code == 403
    assert b"Request must be made with HTMX" in response.content


def test_preserves_view_function_name():
    """Should preserve the original function name using @wraps"""

    @htmx_only_request
    def my_custom_view(request):
        return HttpResponse("OK")

    assert my_custom_view.__name__ == "my_custom_view"


def test_passes_args_and_kwargs(htmx_request):
    """Should pass through args and kwargs to the decorated view"""

    @htmx_only_request
    def mock_view(request, pk, filter_type=None):
        return HttpResponse(f"pk={pk}, filter={filter_type}")

    response = mock_view(htmx_request, pk=42, filter_type="active")

    assert response.status_code == 200
    assert b"pk=42, filter=active" in response.content
