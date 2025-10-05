import pytest
from django.test import RequestFactory

from django_htmx_tools.utils.htmx import is_htmx


@pytest.fixture
def request_factory():
    """Create a RequestFactory instance"""
    return RequestFactory()


@pytest.fixture
def htmx_request(request_factory):
    """Create an HTMX request"""
    request = request_factory.get("/test/", HTTP_HX_REQUEST="true")
    return request


@pytest.fixture
def non_htmx_request(request_factory):
    """Create a non-HTMX request"""
    request = request_factory.get("/test/")
    return request


def test_is_htmx_returns_true_for_htmx_request(htmx_request):
    """Should return True when Hx-Request header is present"""
    assert is_htmx(htmx_request) is True


def test_is_htmx_returns_false_for_non_htmx_request(non_htmx_request):
    """Should return False when Hx-Request header is not present"""
    assert is_htmx(non_htmx_request) is False
