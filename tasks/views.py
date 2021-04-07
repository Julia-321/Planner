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


class AddTask(LoginRequiredMixin, View):
    login_url = '/accounts/login/' # TODO idk what is this, copy paste

    def get(self, request):
        form = CreateTaskForm()
        return render(request, 'tasks/addTaskForm.html', context={'form': form})

    def post(self, request):
        formData = CreateTaskForm(request.POST)
        if formData.is_valid():
            task = formData.save(commit=False)
            task.user = self.request.user
            print(task.name, task.deadline)
            task.save()
        else:
            print('FORM NOT VALID')
        return HttpResponseRedirect('/tasks')


class EditTask(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):
        form = EditTaskForm(instance=Task.objects.get(id=request.GET['id']))
        return render(request, 'tasks/editTaskForm.html', context={'form': form, 'task_id': request.GET['id']})

    def post(self, request):
        formData = EditTaskForm(request.POST)
        if formData.is_valid():
            task = Task.objects.get(id=request.POST['id'])
            task.name = formData.cleaned_data['name']
            task.description = formData.cleaned_data['description']
            task.deadline = formData.cleaned_data['deadline']
            task.save()
        return HttpResponseRedirect('/tasks')
