"""Миксины для приложения books."""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class AuthorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Разрешает только авторам, модераторам и админам."""

    def test_func(self):
        """Проверяет роль пользователя."""
        return self.request.user.is_authenticated and self.request.user.is_author

    def handle_no_permission(self):
        """Возвращает 403 вместо редиректа."""
        if self.request.user.is_authenticated:
            raise PermissionDenied('Недостаточно прав.')
        return super().handle_no_permission()


class ModeratorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Разрешает только модераторам и админам."""

    def test_func(self):
        """Проверяет роль пользователя."""
        return self.request.user.is_authenticated and self.request.user.is_moderator

    def handle_no_permission(self):
        """Возвращает 403 вместо редиректа."""
        if self.request.user.is_authenticated:
            raise PermissionDenied('Недостаточно прав.')
        return super().handle_no_permission()


class IsOwnerOrModeratorMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Разрешает редактировать/удалять только владельцу или модератору."""

    def test_func(self):
        """Проверяет, что пользователь — владелец или модератор."""
        obj = self.get_object()
        user = self.request.user
        if not user.is_authenticated:
            return False
        if user.is_moderator:
            return True
        return getattr(obj, 'owner_id', None) == user.id

    def handle_no_permission(self):
        """Возвращает 403 вместо редиректа."""
        if self.request.user.is_authenticated:
            raise PermissionDenied('Вы не являетесь владельцем этого объекта.')
        return super().handle_no_permission()
