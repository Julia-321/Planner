from django import forms
from django.forms import ModelForm
from tasks.models import Task


class DateInput(forms.DateInput):
    input_type = 'date'


class CreateTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'type', 'deadline']
        widgets = {'deadline': DateInput}
