from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from tasks.forms import *
from tasks import services
from accounts.consts import HOME_PAGE_DICT


class ShowTasks(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    # redirect_field_name = 'redirect_to'

    def get(self, request):
        profile = self.request.user.profile
        self.request.session['checked'] = HOME_PAGE_DICT[self.request.user.profile.home_view]
        if profile.home_view == 1:
            return redirect('show_tasks_daily')
        elif profile.home_view == 2:
            return redirect('show_tasks_weekly')
        elif profile.home_view == 3:
            return redirect('show_tasks_monthly')

    def post(self, request):
        # print(self.request.POST)

        if 'daily' in request.POST:
            self.request.session['checked'] = 'Daily'
            return redirect('show_tasks_daily')
        elif 'weekly' in request.POST:
            self.request.session['checked'] = 'Weekly'
            return redirect('show_tasks_weekly')
        elif 'monthly' in request.POST:
            self.request.session['checked'] = 'Monthly'
            return redirect('show_tasks_monthly')


class AddTask(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):
        form = CreateTaskForm()
        return render(self.request, 'tasks/addTaskForm.html', context={'form': form})

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
        return render(self.request, 'tasks/editTaskForm.html', context={'form': form, 'task_id': request.GET['id']})

    def post(self, request):
        formData = EditTaskForm(self.request.POST)
        if formData.is_valid():
            task = Task.objects.get(id=self.request.POST['id'])
            task.name = formData.cleaned_data['name']
            task.description = formData.cleaned_data['description']
            task.deadline = formData.cleaned_data['deadline']
            task.save()
        return HttpResponseRedirect('/tasks')


class DeleteTask(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):
        Task.objects.get(id=self.request.GET['id']).delete()
        return HttpResponseRedirect('/tasks')


class ShowTasksDaily(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):
        # print(self.request.session['checked'])
        tasks = services.get_tasks_daily(self.request)
        context = {
            'tasks': tasks,
            'checked': self.request.session.get('checked', default=HOME_PAGE_DICT[self.request.user.profile.home_view])
        }
        return render(self.request, 'tasks/daily.html', context=context)


class ShowTasksWeekly(LoginRequiredMixin, View):
    login_url = 'accounts/login'

    def get(self, request):
        tasks = services.get_tasks_weekly(self.request)
        context = {
            'tasks': tasks,
            'checked': self.request.session.get('checked', default=HOME_PAGE_DICT[self.request.user.profile.home_view])
        }
        return render(self.request, 'tasks/weekly.html', context=context)


class ShowTasksMonthly(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):
        tasks = services.get_tasks_monthly(self.request)
        context = {
            'tasks': tasks,
            'checked': self.request.session.get('checked', default=HOME_PAGE_DICT[self.request.user.profile.home_view])
        }
        return render(self.request, 'tasks/monthly.html', context=context)
