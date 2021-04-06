from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from tasks.models import Task


class ShowTasks(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    # redirect_field_name = 'redirect_to'

    def get(self, request):
        tasks = Task.objects.filter(user=self.request.user)
        print(tasks)
        context = {
            'tasks': tasks
        }
        return render(request, 'tasks/list.html', context=context)
