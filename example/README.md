# django-htmx-tools Example Project

This is a demo Django project showcasing the features of `django-htmx-tools`.

## Features Demonstrated

1. **IsHtmxRequestMixin** - Class-based view mixin that restricts access to HTMX requests only
2. **htmx_only_request decorator** - Function-based view decorator for HTMX-only endpoints
3. **htmx_vary_middleware** - Adds proper `Vary: HX-Request` headers for caching
4. **htmx_auth_middleware** - Handles authentication redirects gracefully for HTMX requests

## Setup Instructions

### 1. Install Dependencies

From the root of the repository:

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the library in editable mode
pip install -e .

# Install Django (if not already installed)
pip install django
```

### 2. Run Migrations

```bash
cd example
python manage.py migrate
```

### 3. Create a Superuser (Optional)

To test the authentication middleware features:

```bash
python manage.py createsuperuser
```

### 4. Run the Development Server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to see the demo.

## What to Try

### Task List Demo (http://127.0.0.1:8000/tasks/)

- **Add tasks**: Uses `IsHtmxRequestMixin` - try accessing `/tasks/create/` directly in your browser (will fail with 403)
- **View task details**: Click on a task title to load details via HTMX using the `htmx_only_request` decorator
- **Toggle completion**: Click the checkbox to update task status
- **Delete tasks**: Click delete button to remove tasks
- **Check headers**: Open browser dev tools and see the `Vary: HX-Request` header added by the middleware

### Protected Content Demo (http://127.0.0.1:8000/protected/)

- **Without login**: Try accessing protected content to see how `htmx_auth_middleware` handles the redirect
- **With login**: Login first, then access protected content successfully

## Project Structure

```
example/
├── manage.py
├── example_project/          # Django project settings
│   ├── settings.py          # Includes django-htmx-tools middleware
│   ├── urls.py
│   └── wsgi.py
└── demo_app/                # Demo app with examples
    ├── models.py            # Simple Task model
    ├── views.py             # Views using mixins and decorators
    ├── urls.py
    └── templates/
        └── demo_app/
            ├── base.html    # Base template with HTMX CDN
            ├── index.html   # Feature documentation
            ├── task_list.html
            └── partials/    # HTMX partial templates
```

## Key Code Examples

### Middleware Configuration (settings.py)

```python
MIDDLEWARE = [
    # ... other middleware
    'django_htmx_tools.middleware.htmx_auth_middleware',
    'django_htmx_tools.middleware.htmx_vary_middleware',
]
```

### Using IsHtmxRequestMixin (views.py)

```python
from django_htmx_tools.views import IsHtmxRequestMixin

class TaskCreateView(IsHtmxRequestMixin, CreateView):
    # This view only accepts HTMX requests
    model = Task
    form_class = TaskForm
    template_name = 'demo_app/partials/task_form.html'
```

### Using htmx_only_request Decorator (views.py)

```python
from django_htmx_tools.views.decorators import htmx_only_request

@htmx_only_request
def task_detail(request, pk):
    # This view only accepts HTMX requests
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'demo_app/partials/task_detail.html', {'task': task})
```

## Learning Resources

- [HTMX Documentation](https://htmx.org/docs/)
- [django-htmx-tools on GitHub](https://github.com/howieweiner/django-htmx-tools)

## Notes

- This example uses SQLite for simplicity
- HTMX is loaded from CDN in the base template
- Minimal CSS is included for demonstration purposes
- This example is NOT included in the PyPI package (development/documentation only)
