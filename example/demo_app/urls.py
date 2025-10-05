from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/', views.TaskListView.as_view(), name='task-list'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/', views.task_detail, name='task-detail'),
    path('auth-demo/', views.auth_demo, name='auth-demo'),
    path('protected/', views.protected_content, name='protected-content'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
