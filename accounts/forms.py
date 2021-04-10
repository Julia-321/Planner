from django import forms
from accounts.models import Profile


class SettingsForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('notification_option', 'home_view', 'theme', 'date_view')

