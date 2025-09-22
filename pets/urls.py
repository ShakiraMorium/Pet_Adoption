# from django.urls import path
# from django.contrib.auth import views as auth_views
# from .forms import CustomAuthenticationForm
# from . import views

# app_name = 'accounts'

# urlpatterns = [
#     path('register/', views.RegisterView.as_view(), name='register'),
#     path('activate/<uidb64>/<token>/', views.ActivateView.as_view(), name='activate'),
#     path('login/', auth_views.LoginView.as_view(authentication_form=CustomAuthenticationForm, template_name='registration/login.html'), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
#     path('profile/', views.ProfileView.as_view(), name='profile'),
#     path('deposit/', views.DepositView.as_view(), name='deposit'),
#     path('password-change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
#     path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
# # ]