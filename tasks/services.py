from datetime import timedelta
from tasks.models import Task
from django.utils import timezone


def get_tasks_daily(request, date):

    today = date
    tasks = Task.objects.filter(user=request.user, deadline__year=today.year,
                                deadline__day=today.day).order_by('deadline')
    return tasks


def get_tasks_weekly(request, date):
    today = date
    start = today - timedelta(days=today.weekday())  # the first day of the current week
    end = start + timedelta(days=6)  # the last day of the current week

    tasks = Task.objects.filter(user=request.user, deadline__year=start.year, deadline__month=start.month,
                                deadline__day__range=[start.day, end.day]).order_by('deadline')

    return tasks


def get_tasks_monthly(request, date):
    today = date
    start = today.replace(day=1)
    end = today.replace(day=1).replace(month=today.month+1) - timedelta(days=1)

    tasks = Task.objects.filter(user=request.user, deadline__year=start.year, deadline__month=start.month,
                                deadline__day__range=[start.day, end.day]).order_by('deadline')

    return tasks


def get_date_obj(year: int, month: int, day: int) -> timezone.datetime.date:
    return timezone.datetime(year=year, month=month, day=day).date()
