from django.shortcuts import render
from TestApp.models import Task


# Create your views here.
def tasks_page(request):
    tasks = Task.objects.all()
    context = {
        'tasks': tasks
    }

    return render(request, 'tasks.html', context=context)


def log_in_page(request):
    return render(request, 'log_in/sign_in.html')
