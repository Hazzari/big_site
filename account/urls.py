from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views

app_name = 'account'

urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='account/registration/login.html', ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/registration/logged_out.html'), name='logout'),
    path('', views.dashboard, name='dashboard'),

    # change password urls
    # path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(
             template_name='account/registration/password_change_form.html',
             success_url=reverse_lazy('account:password_change_done')),
         name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # reset password urls
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='account/registration/password_reset_form.html',
             subject_template_name='account/registration/reset_password/password_reset_email_header.txt',
             email_template_name='account/registration/reset_password/password_reset_email_body.txt',
             success_url=reverse_lazy('account:password_reset_done')
         ),
         name='password_reset'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='account/registration/password_reset_done.html',
         ),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='account/registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/registration/password_reset_complete.html',
    ), name='password_reset_complete'),

    # register
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
]
