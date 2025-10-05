# django-htmx-tools
An assortment of Django mixins and middleware for working with HTMX

## Installation

Install directly from GitHub:

```bash
pip install git+https://github.com/howieweiner/django-htmx-tools.git
```

## Features

- `IsHtmxRequestMixin` - Class-based view mixin for HTMX-only endpoints
- `htmx_only_request` - Function decorator for HTMX-only views
- `htmx_vary_middleware` - Proper caching headers for HTMX requests
- `htmx_auth_middleware` - Authentication redirect handling for HTMX

## Example Project

See the [example/](example/) directory for a complete Django project demonstrating all features.

Quick start:
```bash
cd example
python manage.py migrate
python manage.py runserver
```

Visit http://127.0.0.1:8000/ for interactive demos and documentation.

## Development

This project uses [uv](https://docs.astral.sh/uv/) for Python environment management.

### Setup

```bash
source .venv/bin/activate
uv pip install -e ".[dev]"
```

### Run tests

```bash
uv run pytest
```
