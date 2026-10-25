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
from django.views.generic import DetailView, ListView


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

class UserListView(ListView):
    """Список всех пользователей."""

    model = CustomUser
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        """Сортирует по дате регистрации."""
        return CustomUser.objects.order_by('-created_at')


class UserDetailView(DetailView):
    """Публичный профиль пользователя."""

    model = CustomUser
    template_name = 'users/user_detail.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        """Добавляет книги и отзывы пользователя."""
        ctx = super().get_context_data(**kwargs)
        user_obj = self.object
        ctx['books'] = user_obj.books.filter(is_active=True)[:5]
        ctx['reviews'] = user_obj.reviews.select_related('book')[:5]
        return ctx
