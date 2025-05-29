from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('password-change/', views.change_password_view, name='password_change'),
    path('password-change/done/', views.password_change_done_view, name='password_change_done'),
    path('update-preferences/', views.update_preferences, name='update_preferences'),
    path('deactivate-account/', views.deactivate_account, name='deactivate_account'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('activity/', views.activity_view, name='activity'),
]