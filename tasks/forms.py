from django.forms import ModelForm, DateTimeInput
from tasks.models import Task


class CreateTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'deadline']
        widgets = {'deadline': DateTimeInput}


class EditTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'deadline', 'id']
        widgets = {'deadline': DateTimeInput}
