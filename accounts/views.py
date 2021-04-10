from django.shortcuts import render
from django.views import View
from accounts.forms import SettingsForm
from accounts import services


class SettingsView(View):

    def get(self, request):
        context = {
            'form': SettingsForm(),
            'saved': False
        }
        return render(self.request, 'accounts/settings.html', context=context)

    def post(self, request):

        form = SettingsForm(self.request.POST)
        if form.is_valid():
            services.apply_changes(self.request, form)

        context = {
            'form': SettingsForm(),
            'saved': form.is_valid()
        }

        return render(self.request, 'accounts/settings.html', context=context)
