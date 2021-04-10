from django.urls import path, include
from tasks.views import *
from django.views.generic import RedirectView

urlpatterns = [
    path('', ShowTasks.as_view(), name='list_view'),
    path('add/', AddTask.as_view(), name='add_task'),
    path('edit/', EditTask.as_view(), name='edit_task'),
    path('delete/', DeleteTask.as_view(), name='delete_task'),
    path('daily/', ShowTasksDaily.as_view(), name='show_tasks_daily'),
]
