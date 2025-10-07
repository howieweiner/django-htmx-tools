from urllib.parse import urlparse

from django.utils.cache import patch_vary_headers

from django_htmx_tools.utils import is_htmx


def htmx_auth_middleware(get_response):
    """
    Middleware to handle HTMX authentication redirects.

    When an HTMX request receives a 302 redirect to a login page, this middleware
    converts it to a 204 response with an HX-Redirect header. This ensures HTMX
    properly handles the redirect on the client side, preserving the original
    request path in the 'next' query parameter.

    Reference: https://www.caktusgroup.com/blog/2022/11/11/how-handle-django-login-redirects-htmx/

    Args:
        get_response: The next middleware or view in the chain.

    Returns:
        A middleware function that processes HTMX authentication redirects.
    """

    def middleware(request):
        response = get_response(request)
        # HTMX request returning 302 likely is login required. Check url and if so
        # take the redirect location and send it as the HX-Redirect header value,
        # with 'next' query param set to where the request originated. Also change
        # response status code to 204 (no content) so that htmx will obey the
        # HX-Redirect header value.
        if is_htmx(request) and response.status_code == 302 and "login" in response.url:
            ref_header = request.headers.get("Referer", "")
            if ref_header:
                referer = urlparse(ref_header)
                querystring = f"?next={referer.path}"
            else:
                querystring = ""

            redirect = urlparse(response["location"])
            response.status_code = 204
            response.headers["HX-Redirect"] = f"{redirect.path}{querystring}"
        return response

    return middleware


def htmx_vary_middleware(get_response):
    """
    Middleware to add Vary headers for HTMX requests.

    Adds 'HX-Request' to the Vary header for HTMX requests.
    Required if the server renders the full HTML when the HX-Request header is missing/ false,
    but renders a fragment of that HTML when HX-Request is true.

    Reference: https://htmx.org/docs/#caching

    Args:
        get_response: The next middleware or view in the chain.

    Returns:
        A middleware function that patches Vary headers for HTMX requests.
    """

    def middleware(request):
        response = get_response(request)
        if is_htmx(request):
            patch_vary_headers(response, ("HX-Request",))
        return response

    return middleware
