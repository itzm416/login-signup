from django.urls import path, include
from proapp import views

urlpatterns = [
    path('', views.home, name='home'),
  
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('social-auth/', include('social_django.urls', namespace="social")),

    path('signup/', views.user_signup, name='signup'),
    path('account-verify/<slug:token>', views.user_account_verify, name='account-verify'),

    path('password-change/', views.user_password_change, name='change-password'),
    path('password-reset/<slug:token>', views.user_password_reset, name='reset-password'),
    path('user-email-send/', views.user_email_send, name='send-email'),
    
    ]