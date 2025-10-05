import pytest
from django.http import HttpResponse, HttpResponseRedirect
from django.test import RequestFactory

from django_htmx_tools.middleware.htmx import htmx_auth_middleware, htmx_vary_middleware


@pytest.fixture
def request_factory():
    """Create a RequestFactory instance"""
    return RequestFactory()


@pytest.fixture
def htmx_request(request_factory):
    """Create an HTMX request"""
    request = request_factory.get(
        "/test/",
        HTTP_HX_REQUEST="true",
    )
    return request


@pytest.fixture
def non_htmx_request(request_factory):
    """Create a non-HTMX request"""
    request = request_factory.get("/test/")
    return request


@pytest.fixture
def htmx_request_with_referer(request_factory):
    """Create an HTMX request with a Referer header"""
    request = request_factory.get(
        "/test/",
        HTTP_HX_REQUEST="true",
        HTTP_REFERER="http://testserver/previous-page/",
    )
    return request


class TestHtmxAuthMiddleware:
    """Tests for htmx_auth_middleware"""

    def test_converts_302_login_redirect_to_204_with_hx_redirect(self, htmx_request):
        """Should convert 302 login redirects to 204 with HX-Redirect header"""

        def get_response(request):
            response = HttpResponseRedirect("/accounts/login/")
            return response

        middleware = htmx_auth_middleware(get_response)
        response = middleware(htmx_request)

        assert response.status_code == 204
        assert response.headers["HX-Redirect"] == "/accounts/login/"

    def test_includes_next_param_when_referer_present(self, htmx_request_with_referer):
        """Should include 'next' query param from Referer header"""

        def get_response(request):
            return HttpResponseRedirect("/accounts/login/")

        middleware = htmx_auth_middleware(get_response)
        response = middleware(htmx_request_with_referer)

        assert response.status_code == 204
        assert (
            response.headers["HX-Redirect"] == "/accounts/login/?next=/previous-page/"
        )

    def test_does_not_modify_non_htmx_302_redirect(self, non_htmx_request):
        """Should not modify 302 redirects for non-HTMX requests"""

        def get_response(request):
            return HttpResponseRedirect("/accounts/login/")

        middleware = htmx_auth_middleware(get_response)
        response = middleware(non_htmx_request)

        assert response.status_code == 302
        assert "HX-Redirect" not in response.headers
        assert response["Location"] == "/accounts/login/"

    def test_does_not_modify_302_redirect_without_login(self, htmx_request):
        """Should not modify 302 redirects that don't contain 'login'"""

        def get_response(request):
            return HttpResponseRedirect("/some/other/path/")

        middleware = htmx_auth_middleware(get_response)
        response = middleware(htmx_request)

        assert response.status_code == 302
        assert "HX-Redirect" not in response.headers
        assert response["Location"] == "/some/other/path/"

    def test_does_not_modify_non_302_responses(self, htmx_request):
        """Should not modify non-302 responses"""

        def get_response(request):
            return HttpResponse("Success", status=200)

        middleware = htmx_auth_middleware(get_response)
        response = middleware(htmx_request)

        assert response.status_code == 200
        assert "HX-Redirect" not in response.headers
        assert response.content == b"Success"

    def test_handles_login_in_url_path(self, htmx_request):
        """Should handle various login URL patterns"""

        def get_response(request):
            return HttpResponseRedirect("/login")

        middleware = htmx_auth_middleware(get_response)
        response = middleware(htmx_request)

        assert response.status_code == 204
        assert response.headers["HX-Redirect"] == "/login"

    def test_handles_request_without_referer_header(self, htmx_request):
        """Should handle HTMX requests without a Referer header"""

        def get_response(request):
            return HttpResponseRedirect("/accounts/login/")

        middleware = htmx_auth_middleware(get_response)
        response = middleware(htmx_request)

        assert response.status_code == 204
        assert response.headers["HX-Redirect"] == "/accounts/login/"
        assert "next" not in response.headers["HX-Redirect"]


class TestHtmxVaryMiddleware:
    """Tests for htmx_vary_middleware"""

    def test_adds_vary_header_for_htmx_request(self, htmx_request):
        """Should add HX-Request to Vary header for HTMX requests"""

        def get_response(request):
            return HttpResponse("Success")

        middleware = htmx_vary_middleware(get_response)
        response = middleware(htmx_request)

        assert response.status_code == 200
        assert "Vary" in response.headers
        assert "HX-Request" in response.headers["Vary"]

    def test_does_not_add_vary_header_for_non_htmx_request(self, non_htmx_request):
        """Should not add Vary header for non-HTMX requests"""

        def get_response(request):
            return HttpResponse("Success")

        middleware = htmx_vary_middleware(get_response)
        response = middleware(non_htmx_request)

        assert response.status_code == 200
        assert "Vary" not in response.headers

    def test_preserves_existing_vary_headers(self, htmx_request):
        """Should preserve existing Vary headers when adding HX-Request"""

        def get_response(request):
            response = HttpResponse("Success")
            response["Vary"] = "Accept-Language"
            return response

        middleware = htmx_vary_middleware(get_response)
        response = middleware(htmx_request)

        assert response.status_code == 200
        assert "Vary" in response.headers
        vary_values = [v.strip() for v in response.headers["Vary"].split(",")]
        assert "Accept-Language" in vary_values
        assert "HX-Request" in vary_values

    def test_does_not_duplicate_hx_request_in_vary(self, htmx_request):
        """Should not duplicate HX-Request if already in Vary header"""

        def get_response(request):
            response = HttpResponse("Success")
            response["Vary"] = "HX-Request"
            return response

        middleware = htmx_vary_middleware(get_response)
        response = middleware(htmx_request)

        assert response.status_code == 200
        vary_header = response.headers["Vary"]
        assert vary_header.count("HX-Request") == 1
