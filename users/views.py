"""Views для приложения users (FBV)."""
from django.contrib.auth import (
    authenticate, login, logout, update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import (
    CustomPasswordChangeForm,
    UserLoginForm,
    UserRegisterForm,
    UserUpdateForm,
)
from .services import send_password_change_email, send_welcome_email


def register_view(request):
    """Регистрация нового пользователя."""
    if request.user.is_authenticated:
        return redirect('users:profile')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_welcome_email(user)
            login(request, user)
            return redirect('users:profile')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """Вход в аккаунт."""
    if request.user.is_authenticated:
        return redirect('users:profile')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('users:profile')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """Выход из аккаунта."""
    logout(request)
    return redirect('users:login')


@login_required
def profile_view(request):
    """Просмотр и редактирование профиля."""
    if request.method == 'POST':
        form = UserUpdateForm(
            request.POST, request.FILES, instance=request.user,
        )
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})


@login_required
def password_change_view(request):
    """Смена пароля авторизованным пользователем."""
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            send_password_change_email(user)
            return redirect('users:profile')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'users/password_change.html', {'form': form})
