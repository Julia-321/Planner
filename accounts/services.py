from accounts.forms import SettingsForm
from accounts.models import Profile


def apply_changes(request, form: SettingsForm):
    cd = form.cleaned_data

    profile: Profile = Profile.objects.get(user=request.user)

    profile.notification_option = cd['notification_option']
    profile.home_view = cd['home_view']
    profile.theme = cd['theme']

    profile.save()
