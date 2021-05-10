from datetime import timedelta
from tasks.models import Task
from django.utils import timezone
from accounts.consts import DAYS, MONTHS
from calendar import Calendar
from dateutil.relativedelta import relativedelta


def get_tasks_daily(request, date):

    today = date
    tasks = Task.objects.filter(user=request.user, deadline__year=today.year, deadline__month=today.month,
                                deadline__day=today.day).order_by('complete', 'deadline')
    return tasks


def get_tasks_weekly(request, date):
    today = date
    start = today - timedelta(days=today.weekday())  # the first day of the current week
    end = start + timedelta(days=6)  # the last day of the current week

    tasks = Task.objects.filter(user=request.user, deadline__year=start.year, deadline__month=start.month,
                                deadline__day__range=[start.day, end.day]).order_by('complete', 'deadline')
    # res = [ (day, date, queryset), ... ]
    res = []

    cur: timezone.datetime.date = start
    for day in DAYS:
        res += [(day, f'{MONTHS[cur.month - 1]} {cur.day}', tasks.filter(deadline__day=cur.day))]
        cur += timedelta(days=1)
    return res


def get_tasks_monthly(request, date):
    print('---------------------------------')
    today = date
    start = today.replace(day=1)
    print('-------------', request, date)
    end = (today + relativedelta(months=+1)).replace(day=1) - timedelta(days=1)

    tasks = Task.objects.filter(user=request.user, deadline__year=start.year, deadline__month=start.month,
                                deadline__day__range=[start.day, end.day]).order_by('complete', 'deadline')

    # cur = start
    # res = []
    # while cur <= end:
    #     res += [(DAYS[cur.weekday()], f'{MONTHS[cur.month - 1]} {cur.day}', tasks.filter(deadline__day=cur.day))]
    #     cur += timedelta(days=1)
    res = Calendar().monthdayscalendar(today.year, today.month)

    return list(map(lambda item: list(map(lambda x: (x, tasks.filter(deadline__day=x)) if x else (x, []), item)), res))


def get_date_obj(year: int, month: int, day: int) -> timezone.datetime.date:
    return timezone.datetime(year=year, month=month, day=day).date()
