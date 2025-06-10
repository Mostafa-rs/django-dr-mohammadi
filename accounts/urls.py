"""
Accounts URLs
Mostafa Rasouli
mostafarasooli54@gmail.com
feb 2024
"""

from django.urls import path

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('login/confirm/', views.UserLoginConfirmView.as_view(), name='login_confirm'),
]