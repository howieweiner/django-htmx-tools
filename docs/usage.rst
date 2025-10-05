Usage
=====

View Mixins
-----------

IsHtmxRequestMixin
~~~~~~~~~~~~~~~~~~

Use this mixin to ensure that a class-based view only accepts HTMX requests:

.. code-block:: python

   from django.views.generic import TemplateView
   from django_htmx_tools.views.mixins import IsHtmxRequestMixin

   class MyHtmxView(IsHtmxRequestMixin, TemplateView):
       template_name = 'my_template.html'

If a non-HTMX request is made to this view, it will return a 403 Forbidden response.

View Decorators
---------------

htmx_only_request
~~~~~~~~~~~~~~~~~

For function-based views, use the ``htmx_only_request`` decorator:

.. code-block:: python

   from django_htmx_tools.views.decorators import htmx_only_request

   @htmx_only_request
   def my_htmx_view(request):
       return render(request, 'my_template.html')

Utilities
---------

is_htmx
~~~~~~~

The ``is_htmx`` utility function checks if a request is an HTMX request. This is useful
for conditionally rendering different templates or responses based on the request type:

.. code-block:: python

   from django.views.generic import ListView
   from django_htmx_tools.utils import is_htmx

   class TaskListView(ListView):
       model = Task
       template_name = 'task_list.html'

       def get_template_names(self):
           if is_htmx(self.request):
               # Return partial template for HTMX requests
               return ['partials/task_list_partial.html']
           # Return full page template for normal browser requests
           return [self.template_name]

This pattern allows you to serve full HTML pages for initial page loads and partial
HTML fragments for HTMX-driven updates, enabling progressive enhancement.

Middleware
----------

htmx_vary_middleware
~~~~~~~~~~~~~~~~~~~~

This middleware adds the proper ``Vary`` header for HTMX requests to ensure
proper caching behavior. It adds ``Vary: HX-Request`` to responses.

Add it to your ``MIDDLEWARE`` setting:

.. code-block:: python

   MIDDLEWARE = [
       # ... other middleware
       'django_htmx_tools.middleware.htmx.htmx_vary_middleware',
   ]

htmx_auth_middleware
~~~~~~~~~~~~~~~~~~~~

This middleware handles authentication redirects for HTMX requests. Instead of
redirecting to a login page (which would be problematic for HTMX), it returns
a 403 Forbidden response with proper HTMX headers.

Add it to your ``MIDDLEWARE`` setting:

.. code-block:: python

   MIDDLEWARE = [
       # ... other middleware
       'django_htmx_tools.middleware.htmx.htmx_auth_middleware',
   ]

Example Project
---------------

See the `example/ <https://github.com/howieweiner/django-htmx-tools/tree/main/example>`_
directory in the repository for a complete Django project demonstrating all features.

Quick start:

.. code-block:: bash

   cd example
   python manage.py migrate
   python manage.py runserver

Visit http://127.0.0.1:8000/ for interactive demos and documentation.
