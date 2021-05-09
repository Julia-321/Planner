from django.contrib.auth.models import User
import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from tasks.forms import *
from tasks import services
from accounts.consts import HOME_PAGE_DICT
from django.urls import reverse
from webpush import send_user_notification
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST


class ShowTasks(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    @csrf_exempt
    def get(self, request):

        payload = {'head': 'head_data', 'body': 'body_data'}
        user = User.objects.get(id=self.request.user.id)
        send_user_notification(user=user, payload=payload, ttl=1000)
        print(user, type(user))
        year = timezone.now().year
        month = timezone.now().month
        day = timezone.now().day
        kwargs = {'year': year, 'month': month, 'day': day}
        # print(year, month, day)
        profile = self.request.user.profile
        self.request.session['checked'] = HOME_PAGE_DICT[self.request.user.profile.home_view]
        if profile.home_view == 1:
            return redirect(reverse('show_tasks_daily', kwargs=kwargs))
        elif profile.home_view == 2:
            return redirect(reverse('show_tasks_weekly',  kwargs=kwargs))
        elif profile.home_view == 3:
            return redirect(reverse('show_tasks_monthly',  kwargs=kwargs))

    def post(self, request, year, month, day):

        kwargs = {'year': year, 'month': month, 'day': day}
        cur_date = datetime.date(year=year, month=month, day=day)
        print(request.POST)

        if 'daily' in self.request.POST or request.POST.get('cur') == 'Daily':
            self.request.session['checked'] = 'Daily'

            if 'next' in request.POST:
                res_date = cur_date + relativedelta(days=+1)
                kwargs = {'year': res_date.year, 'month': res_date.month, 'day': res_date.day}
            if 'prev' in request.POST:
                res_date = cur_date + relativedelta(days=-1)
                kwargs = {'year': res_date.year, 'month': res_date.month, 'day': res_date.day}
            if 'complete' or 'incomplete' in request.POST:
                task = Task.objects.get(id=int(request.POST.get('complete_id')))
                task.complete = not task.complete
                task.save()

            return redirect(reverse('show_tasks_daily', kwargs=kwargs))
        elif 'weekly' in self.request.POST or request.POST.get('cur') == 'Weekly':
            self.request.session['checked'] = 'Weekly'
            if 'next' in request.POST:
                res_date = cur_date + relativedelta(weeks=+1)
                kwargs = {'year': res_date.year, 'month': res_date.month, 'day': res_date.day}
            if 'prev' in request.POST:
                res_date = cur_date + relativedelta(weeks=-1)
                kwargs = {'year': res_date.year, 'month': res_date.month, 'day': res_date.day}
            return redirect(reverse('show_tasks_weekly',  kwargs=kwargs))
        elif 'monthly' in self.request.POST or request.POST.get('cur') == 'Monthly':
            self.request.session['checked'] = 'Monthly'
            if 'next' in request.POST:
                res_date = cur_date + relativedelta(months=+1)
                kwargs = {'year': res_date.year, 'month': res_date.month, 'day': res_date.day}
            if 'prev' in request.POST:
                res_date = cur_date + relativedelta(months=-1)
                kwargs = {'year': res_date.year, 'month': res_date.month, 'day': res_date.day}
            return redirect(reverse('show_tasks_monthly',  kwargs=kwargs))


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

    def get(self, request, year, month, day):
        cur_date = services.get_date_obj(year, month, day)
        tasks = services.get_tasks_daily(self.request, cur_date)
        context = {
            'date': cur_date,
            'tasks': tasks,
            'checked': self.request.session.get('checked', default=HOME_PAGE_DICT[self.request.user.profile.home_view])
        }
        return render(self.request, 'tasks/daily.html', context=context)


class ShowTasksWeekly(LoginRequiredMixin, View):
    login_url = 'accounts/login'

    def get(self, request, year, month, day):
        cur_date = services.get_date_obj(year, month, day)

        tasks = services.get_tasks_weekly(self.request, cur_date)
        context = {
            'date': cur_date,
            'tasks': tasks,
            'checked': self.request.session.get('checked', default=HOME_PAGE_DICT[self.request.user.profile.home_view])
        }
        return render(self.request, 'tasks/weekly.html', context=context)


class ShowTasksMonthly(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, year, month, day):
        cur_date = services.get_date_obj(year, month, day)
        tasks = services.get_tasks_monthly(self.request, cur_date)
        context = {
            'date': cur_date,
            'tasks': tasks,
            'checked': self.request.session.get('checked', default=HOME_PAGE_DICT[self.request.user.profile.home_view])
        }
        return render(self.request, 'tasks/monthly.html', context=context)

