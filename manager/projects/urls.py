from django.urls import path
from django.contrib.auth.models import User
from . import views

urlpatterns = [

    path('dashboard/', views.dashboard, name='dashboard'),
    path('create_project/', views.projectCreate, name='create_project'),
    path('project/<str:pk>/', views.project, name='project'),
    path('detail/', views.projectDetail, name='project_detail'),  
    path('tasks/', views.tasks, name='tasks'),
    path('create_task/<str:pk>', views.taskCreate, name='create_task'),
    path('update_task/<str:pk>/update', views.updateTask, name='update_task'),
    path('delete_task/<str:pk>/delete', views.deleteTask, name='delete_task'),

]