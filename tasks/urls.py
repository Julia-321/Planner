from django.urls import path, include
from tasks.views import *
from django.views.generic import RedirectView

urlpatterns = [
    path('', ShowTasks.as_view(), name='list_view'),
    path('add/', AddTask.as_view()),
    path('edit/', EditTask.as_view())

]
