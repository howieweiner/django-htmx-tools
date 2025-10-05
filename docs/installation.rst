Installation
============

PyPI Installation
-----------------

Once published, you can install django-htmx-tools from PyPI:

.. code-block:: bash

   pip install django-htmx-tools

GitHub Installation
-------------------

Install directly from GitHub:

.. code-block:: bash

   pip install git+https://github.com/howieweiner/django-htmx-tools.git

Requirements
------------

- Python 3.10 or higher
- Django 4.2 or higher

Configuration
-------------

Add the middleware to your Django settings:

.. code-block:: python

   # settings.py

   MIDDLEWARE = [
       # ... other middleware
       'django_htmx_tools.middleware.htmx.htmx_vary_middleware',
       'django_htmx_tools.middleware.htmx.htmx_auth_middleware',
   ]

