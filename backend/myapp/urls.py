# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('ask-code/', views.AskCodeView.as_view(), name='ask_code'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('send-code/', views.SendCodeView.as_view(), name='send_code'),
    path('verify-code/', views.VerifyCodeView.as_view(), name='verify_code'),
]