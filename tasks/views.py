import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import Profile
from tasks.forms import *
from tasks import services
from accounts.consts import HOME_PAGE_DICT, MONTHS
from django.urls import reverse


class ShowTasks(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):
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
            if 'complete' in request.POST or 'incomplete' in request.POST:
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
            if 'complete' in request.POST or 'incomplete' in request.POST:
                task = Task.objects.get(id=int(request.POST.get('complete_id')))
                task.complete = not task.complete
                task.save()

            return redirect(reverse('show_tasks_weekly',  kwargs=kwargs))
        elif 'monthly' in self.request.POST or request.POST.get('cur') == 'Monthly':
            self.request.session['checked'] = 'Monthly'
            if 'next' in request.POST:
                res_date = cur_date + relativedelta(months=+1)
                kwargs = {'year': res_date.year, 'month': res_date.month, 'day': res_date.day}
            if 'prev' in request.POST:
                res_date = cur_date + relativedelta(months=-1)
                kwargs = {'year': res_date.year, 'month': res_date.month, 'day': res_date.day}
            if 'complete' in request.POST or 'incomplete' in request.POST:
                task = Task.objects.get(id=int(request.POST.get('complete_id')))
                task.complete = not task.complete
                task.save()

            return redirect(reverse('show_tasks_monthly',  kwargs=kwargs))


class AddTaskView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):
        return render(self.request, 'tasks/addTask.html')

    def post(self, request):
        title = self.request.POST.get('title')
        description = self.request.POST.get('description')
        task_type = int(self.request.POST.get('type'))

        if self.request.POST.get('deadline_date'):
            deadline_date = timezone.datetime.strptime(self.request.POST.get('deadline_date'), '%Y-%m-%d')
        else:
            deadline_date = timezone.datetime.now().date()

        if self.request.POST.get('deadline_time'):
            deadline_time = timezone.datetime.strptime(self.request.POST.get('deadline_time'), '%H:%M').time()
        else:
            deadline_time = timezone.datetime.now().time()

        Task.objects.create(user=self.request.user,
                            name=title,
                            description=description,
                            type=task_type,
                            deadline=timezone.datetime.combine(deadline_date, deadline_time) or timezone.now())
        return redirect('list_view')


class EditTaskView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):
        pk = self.request.GET.get('id')
        task = Task.objects.get(id=pk)
        deadline_date = task.deadline.date().strftime('%Y-%m-%d')
        deadline_time = task.deadline.time().strftime('%H:%M')
        return render(self.request, 'tasks/editTask.html', context={'task': task, 'deadline_date': deadline_date,
                                                                    'deadline_time': deadline_time})

    def post(self, request, pk):
        task = get_object_or_404(Task, id=pk)
        task.name = self.request.POST.get('title')
        task.description = self.request.POST.get('description')
        # task.type = int(self.request.POST.get('type'))

        if self.request.POST.get('deadline_date'):
            deadline_date = timezone.datetime.strptime(self.request.POST.get('deadline_date'), '%Y-%m-%d')
        else:
            deadline_date = timezone.datetime.now().date()

        if self.request.POST.get('deadline_time'):
            deadline_time = timezone.datetime.strptime(self.request.POST.get('deadline_time'), '%H:%M').time()
        else:
            deadline_time = timezone.datetime.now().time()
        task.deadline = datetime.datetime.combine(deadline_date, deadline_time)
        task.save()
        return redirect('list_view')


# class AddTask(LoginRequiredMixin, View):
#     login_url = '/accounts/login/'
#
#     def get(self, request):
#         form = CreateTaskForm()
#         return render(self.request, 'tasks/addTask.html', context={'form': form})
#
#     def post(self, request):
#         formData = CreateTaskForm(request.POST)
#         if formData.is_valid():
#             task = formData.save(commit=False)
#             task.user = self.request.user
#             print(task.name, task.deadline)
#             task.save()
#         else:
#             print('FORM NOT VALID')
#         return HttpResponseRedirect('/tasks')


# class EditTask(LoginRequiredMixin, View):
#     login_url = '/accounts/login/'
#
#     def get(self, request):
#         form = EditTaskForm(instance=Task.objects.get(id=request.GET['id']))
#         return render(self.request, 'tasks/editTask.html', context={'form': form, 'task_id': request.GET['id']})
#
#     def post(self, request):
#         formData = EditTaskForm(self.request.POST)
#         if formData.is_valid():
#             task = Task.objects.get(id=self.request.POST['id'])
#             task.name = formData.cleaned_data['name']
#             task.description = formData.cleaned_data['description']
#             task.deadline = formData.cleaned_data['deadline']
#             task.save()
#         return HttpResponseRedirect('/tasks')


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
        print(tasks)
        context = {
            'date': cur_date,
            'tasks': tasks,
            'checked': self.request.session.get('checked', default=HOME_PAGE_DICT[self.request.user.profile.home_view]),
            'month_name': MONTHS[month - 1],
        }
        return render(self.request, 'tasks/monthly.html', context=context)


class PushView(LoginRequiredMixin, View):
    login_url = 'accounts/login'

    def get(self, request):
        date = timezone.now().date()
        push_time = Profile.objects.get(user=self.request.user).push_time
        if push_time == 1:  # deadline
            return Task.objects.filter(user=self.request.user, deadline=date)
        elif push_time == 2:  # 15 min
            return Task.objects.filter(user=self.request.user, deadline=date+timezone.timedelta(minutes=15))
        elif push_time == 3:  # 1 hour
            return Task.objects.filter(user=self.request.user, deadline=date+timezone.timedelta(hours=1))
        else:  # push_time == 4:  # 1 min
            return Task.objects.filter(user=self.request.user, deadline=date+timezone.timedelta(minutes=1))
