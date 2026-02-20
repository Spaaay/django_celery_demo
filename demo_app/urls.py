from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('trigger-task/', views.trigger_task),
    path('trigger-retry/', views.trigger_retry_task),
    path('trigger-workflow/', views.trigger_workflow),
    path('task-status/<str:task_id>/', views.get_task_status),
    path('cache-test/', views.cache_test),
    path('react-users/', views.get_react_users),
]
