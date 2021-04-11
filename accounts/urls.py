from django.urls import path
from accounts.views import SettingsView, SignUpView


urlpatterns = [
    path('settings/', SettingsView.as_view(), name='settings'),
    path('signup/', SignUpView.as_view(), name='sign_up'),
]
