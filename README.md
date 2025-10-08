# django-htmx-tools

[![PyPI version](https://badge.fury.io/py/django-htmx-tools.svg)](https://badge.fury.io/py/django-htmx-tools)
[![Python versions](https://img.shields.io/pypi/pyversions/django-htmx-tools.svg)](https://pypi.org/project/django-htmx-tools/)
[![Django versions](https://img.shields.io/pypi/djversions/django-htmx-tools.svg)](https://pypi.org/project/django-htmx-tools/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/django-htmx-tools/badge/?version=latest)](https://django-htmx-tools.readthedocs.io/en/latest/?badge=latest)

An assortment of Django mixins and middleware for working with HTMX.

django-htmx-tools provides a collection of utilities to make it easier to build
HTMX-powered Django applications. It includes middleware for proper caching and
authentication handling, as well as mixins and decorators for protecting views.

## Features

- **IsHtmxRequestMixin** - Class-based view mixin for HTMX-only endpoints
- **htmx_only_request** - Function decorator for HTMX-only views
- **is_htmx** - Utility function to check if a request is from HTMX
- **htmx_vary_middleware** - Proper caching headers for HTMX requests
- **htmx_auth_middleware** - Authentication redirect handling for HTMX

## References

- [HTMX Caching](https://htmx.org/docs/#caching)
- [How to Handle Django Login Redirects with HTMX](https://www.caktusgroup.com/blog/2022/11/11/how-handle-django-login-redirects-htmx/)

## Documentation

Please visit [https://django-htmx-tools.readthedocs.io](https://django-htmx-tools.readthedocs.io)
