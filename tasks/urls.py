from django.urls import path, include
from tasks.views import *
from django.views.generic import RedirectView

urlpatterns = [
    path('', ShowTasks.as_view(), name='list_view'),  # get method
    path('<int:year>/<int:month>/<int:day>/', ShowTasks.as_view(), name='list_view'),  # post method
    path('add/', AddTaskView.as_view(), name='add_task'),
    path('edit/', EditTaskView.as_view(), name='edit_task'),
    path('edit/<int:pk>', EditTaskView.as_view(), name='edit_task'),
    path('delete/', DeleteTask.as_view(), name='delete_task'),
    path('daily/<int:year>/<int:month>/<int:day>/', ShowTasksDaily.as_view(), name='show_tasks_daily'),
    path('weekly/<int:year>/<int:month>/<int:day>/', ShowTasksWeekly.as_view(), name='show_tasks_weekly'),
    path('monthly/<int:year>/<int:month>/<int:day>/', ShowTasksMonthly.as_view(), name='show_tasks_monthly'),
]
