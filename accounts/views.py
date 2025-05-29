from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm, CustomPasswordChangeForm
from .models import Profile 
from django.contrib.auth.views import LoginView
from .forms import LoginForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.views.decorators.http import require_http_methods, require_POST
from django.http import JsonResponse
import json
from classifier.models import AnalysisHistory
from .utils import send_welcome_email, send_profile_update_notification, send_password_change_notification



def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Envoi de l'email de bienvenue
            send_welcome_email(user)
            
            messages.success(request, 'Registration successful!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Welcome back! You have been successfully logged in.')
            return redirect('home')
        else:
            if form.non_field_errors():
                messages.error(request, 'Invalid username or password. Please try again.')
            else:
                messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('landing') 

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            
            # Envoi de notification de mise à jour du profil
            send_profile_update_notification(request.user)
            
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            
            # Envoi de notification de changement de mot de passe
            send_password_change_notification(user)
            
            messages.success(request, 'Your password has been successfully changed!')
            return redirect('accounts:password_change_done')
        else:
            if form.errors.get('old_password'):
                messages.error(request, 'Current password is incorrect.')
            elif form.errors.get('new_password2'):
                messages.error(request, 'The two password fields do not match.')
            else:
                messages.error(request, 'Please correct the errors below.')
            print(f"Form errors: {form.errors}")
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'accounts/password_change.html', {'form': form})


@login_required
def password_change_done_view(request):
    return render(request, 'accounts/password_change_done.html')


@login_required
@require_POST
def update_preferences(request):
    try:
        profile, created = Profile.objects.get_or_create(user=request.user)
        
        preference = request.POST.get('preference')
        value = request.POST.get('value') == 'true'
        
        if preference == 'email_notifications':
            profile.email_notifications = value
            profile.save()
            return JsonResponse({'success': True, 'message': 'Email notification preference updated.'})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid preference'})
            
    except Exception as e:
        print(f"Error updating preference: {str(e)}")
        return JsonResponse({'success': False, 'error': 'An error occurred while updating your preferences.'})


@login_required
def deactivate_account(request):
    if request.method == 'POST':
        try:
            user = request.user
            user.is_active = False
            user.save()
            logout(request)
            messages.success(request, 'Your account has been deactivated.')
            return redirect('home')
        except Exception as e:
            print(f"Error deactivating account: {str(e)}")
            messages.error(request, 'An error occurred while deactivating your account.')
            return redirect('accounts:profile')
    return redirect('accounts:profile')


@login_required
def delete_account(request):
    if request.method == 'POST':
        try:
            user = request.user
            user.delete()
            logout(request)
            messages.success(request, 'Your account has been permanently deleted.')
            return redirect('home')
        except Exception as e:
            print(f"Error deleting account: {str(e)}")
            messages.error(request, 'An error occurred while deleting your account.')
            return redirect('accounts:profile')
    return redirect('accounts:profile')

@login_required
def activity_view(request):
    analyses = AnalysisHistory.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/activity.html', {'analyses': analyses})