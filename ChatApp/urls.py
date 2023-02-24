from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('update_details', views.update_details, name="update_details"),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('create_group/', views.create_group, name="create_group"),
    path("login/password_reset", views.password_reset, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password/password_reset_complete.html'), name='password_reset_complete'),      
]
