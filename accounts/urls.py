from django.urls import path
from accounts.views import SettingsView, SignUpView, change_password


urlpatterns = [
    path('settings/', SettingsView.as_view(), name='settings'),
    path('signup/', SignUpView.as_view(), name='sign_up'),
    path('password/', change_password, name="change_password")
]
