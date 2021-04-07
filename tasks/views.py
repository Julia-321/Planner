from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from tasks.models import Task
from tasks.forms import *


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


class addTasks(LoginRequiredMixin, View):
    login_url = '/accounts/login/' # TODO idk what is this, copy paste
    def get(self, request):
        form = CreateTaskForm()
        return render(request, 'tasks/addTaskForm.html', context={'form': form})

    def post(self, request):
        submittedForm = CreateTaskForm(request.POST)
        if submittedForm.is_valid():
            task = Task(**submittedForm.cleaned_data)
            task.user = self.request.user
            print(task.name, task.deadline)
            task.save()
        else:
            print('FORM NOT VALID')
        return HttpResponseRedirect('/tasks')



