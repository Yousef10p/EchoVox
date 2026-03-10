from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import LoginForm, RegisterForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('landing')

    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect(request.GET.get('next', 'landing'))
        else:
            messages.error(request, 'Invalid credentials. Please try again.')

    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('landing')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to Echovox, {user.first_name}!')
            return redirect('landing')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')

    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('landing')
