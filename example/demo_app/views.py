from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from django_htmx_tools.utils import is_htmx
from django_htmx_tools.views import IsHtmxRequestMixin
from django_htmx_tools.views.decorators import htmx_only_request
from .models import Task
from .forms import TaskForm


def index(request):
    """Home page with links to all demos."""
    return render(request, 'demo_app/index.html')


class TaskListView(ListView):
    """
    Demonstrates htmx_vary_middleware and is_htmx utility function.

    Uses is_htmx() to determine request type and return appropriate template:
    - Normal browser request: Returns full HTML page with layout
    - HTMX request: Returns only the task list partial for dynamic updates

    The htmx_vary_middleware automatically adds 'Vary: HX-Request' header
    to ensure proper HTTP caching for both response types.
    """
    model = Task
    template_name = 'demo_app/task_list.html'
    context_object_name = 'tasks'

    def get_template_names(self):
        if is_htmx(self.request):
            return ['demo_app/partials/task_list_partial.html']
        return [self.template_name]


class TaskCreateView(IsHtmxRequestMixin, CreateView):
    """
    Demonstrates IsHtmxRequestMixin.

    This view only accepts HTMX requests. Direct browser access returns 403.
    """
    model = Task
    form_class = TaskForm
    template_name = 'demo_app/partials/task_form.html'
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.save()
        # Return the updated task list
        tasks = Task.objects.all()
        return render(self.request, 'demo_app/partials/task_list_partial.html', {'tasks': tasks})


@htmx_only_request
def task_detail(request, pk):
    """
    Demonstrates htmx_only_request decorator.

    This view only accepts HTMX requests. Direct browser access returns 403.
    """
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'demo_app/partials/task_detail.html', {'task': task})


def auth_demo(request):
    """Demo page for testing htmx_auth_middleware."""
    return render(request, 'demo_app/auth_demo.html')


@login_required
def protected_content(request):
    """
    Demonstrates htmx_auth_middleware.

    If accessed via HTMX without authentication, the middleware converts
    the 302 redirect to a 204 with HX-Redirect header, preserving the
    'next' parameter for proper redirect after login.
    """
    return render(request, 'demo_app/partials/protected_content.html')


def login_view(request):
    """Simple login page to demonstrate auth middleware."""
    from django.contrib.auth import authenticate, login

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)

    return render(request, 'demo_app/login.html')


def logout_view(request):
    """Logout and redirect to home."""
    from django.contrib.auth import logout
    logout(request)
    return redirect('index')
