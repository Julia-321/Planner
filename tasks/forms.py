from django import forms
from datetimepicker.widgets import DateTimePicker


class DateInput(forms.DateInput):
    input_type = 'date'


class CreateTaskForm(forms.Form):
    name = forms.CharField()  # TODO parameters
    description = forms.CharField()
    deadline = forms.DateTimeField(widget=DateInput)
    type = forms.ChoiceField(choices=((0, "Event"), (1, "Task")))
