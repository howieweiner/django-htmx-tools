django-htmx-tools
================

An assortment of Django mixins and middleware for working with HTMX.

django-htmx-tools provides a collection of utilities to make it easier to build
HTMX-powered Django applications. It includes middleware for proper caching and
authentication handling, as well as mixins and decorators for protecting views.

Features
--------

- **IsHtmxRequestMixin** - Class-based view mixin for HTMX-only endpoints
- **htmx_only_request** - Function decorator for HTMX-only views
- **is_htmx** - Utility function to check if a request is from HTMX
- **htmx_vary_middleware** - Proper caching headers for HTMX requests
- **htmx_auth_middleware** - Authentication redirect handling for HTMX

Requirements
------------

- Python 3.10+
- Django 4.2+

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
