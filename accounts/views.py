from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect

from django.shortcuts import render
from django.views import View
from accounts.forms import SettingsForm
from accounts import services
from django_registration.backends.one_step.views import RegistrationView
from accounts.models import Profile


class SettingsView(View):

    def get(self, request):
        context = {
            'form': SettingsForm(),
            'saved': False,
            'notification_option': self.request.user.profile.notification_option,
            'home_view': self.request.user.profile.home_view,
            'theme': self.request.user.profile.theme,
            'push_time': self.request.user.profile.push_time,
        }
        print(context)
        return render(self.request, 'accounts/settings.html', context=context)

    def post(self, request):
        form = SettingsForm(self.request.POST)
        if form.is_valid():
            services.apply_changes(self.request, form)

        context = {
            'form': SettingsForm(),
            'saved': form.is_valid(),
            'notification_option': self.request.user.profile.notification_option,
            'home_view': self.request.user.profile.home_view,
            'theme': self.request.user.profile.theme,
            'push_time': self.request.user.profile.push_time,
        }

        return render(self.request, 'accounts/settings.html', context=context)


class SignUpView(RegistrationView):

    def register(self, form):
        new_user = super(SignUpView, self).register(form)
        new_profile = Profile(user=new_user)
        new_profile.save()
        return new_user


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })
