from django.urls import path, include
from tasks.views import ShowTasks
from django.views.generic import RedirectView

urlpatterns = [
    path('', ShowTasks.as_view(), name='list_view'),
]
