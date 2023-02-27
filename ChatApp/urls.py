from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('update_details', views.update_details, name="update_details"),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('create_group/', views.create_group, name="create_group"),
    path('delete_group/<int:group_id>/', views.delete_group, name="delete_group"),
    path('group_detail/<int:group_id>/', views.group_detail, name="group_detail"),
    path("login/password_reset", views.password_reset, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password/password_reset_complete.html'), name='password_reset_complete'),  
    path('search_members/', views.search_members, name='search_members'),
    path('add_member/<int:group_id>/<int:member_id>/', views.add_member, name='add_member'),
    path('groups/<int:group_id>/', views.chat_group, name='group_detail'),
    path('groups/<int:group_id>/send_message/', views.send_message, name='send_message'),
    path('messages/<int:message_id>/add_reaction/', views.add_reaction, name='add_reaction'),    
]
