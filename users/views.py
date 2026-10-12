"""Views для приложения users (CBV)."""
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
)
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import (
    CustomPasswordChangeForm,
    UserLoginForm,
    UserRegisterForm,
    UserUpdateForm,
)
from .models import CustomUser
from .services import send_password_change_email, send_welcome_email


class RegisterView(CreateView):
    """CBV для регистрации нового пользователя."""

    model = CustomUser
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:profile')

    def dispatch(self, request, *args, **kwargs):
        """Перенаправляет авторизованных на профиль."""
        if request.user.is_authenticated:
            return self.redirect_to_profile()
        return super().dispatch(request, *args, **kwargs)

    def redirect_to_profile(self):
        """Возвращает редирект на профиль."""
        from django.shortcuts import redirect
        return redirect('users:profile')

    def form_valid(self, form):
        """Сохраняет пользователя, шлёт письмо и логинит его."""
        response = super().form_valid(form)
        user = self.object
        send_welcome_email(user)
        from django.contrib.auth import login
        login(self.request, user)
        return response


class CustomLoginView(LoginView):
    """CBV для входа в аккаунт."""

    template_name = 'users/login.html'
    authentication_form = UserLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        """Возвращает URL для редиректа после входа."""
        return reverse_lazy('users:profile')


class CustomLogoutView(LogoutView):
    """CBV для выхода из аккаунта."""

    next_page = reverse_lazy('users:login')
    template_name = 'users/logout.html'


class ProfileView(LoginRequiredMixin, UpdateView):
    """CBV для просмотра и редактирования профиля."""

    model = CustomUser
    form_class = UserUpdateForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        """Возвращает текущего пользователя."""
        return self.request.user


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """CBV для смены пароля."""

    form_class = CustomPasswordChangeForm
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        """Сохраняет пароль, обновляет сессию и шлёт письмо."""
        response = super().form_valid(form)
        update_session_auth_hash(self.request, form.user)
        send_password_change_email(form.user)
        return response
