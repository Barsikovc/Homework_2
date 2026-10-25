"""Views для приложения books (CBV)."""
import logging

from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)
from .mixins import (
    AuthorRequiredMixin,
    IsOwnerOrModeratorMixin,
    ModeratorRequiredMixin,
)
from .services import send_new_book_email, send_views_milestone_email
from .forms import AuthorForm, BookForm, BookUpdateForm, BookAdminUpdateForm, GenreForm, ReviewForm
from .models import Author, Book, Genre, Review

logger = logging.getLogger('homework.requests')


# ============ BOOK ============

class BookListView(ListView):
    """Список всех книг."""

    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        """Оптимизирует запрос."""
        return Book.objects.select_related('genre', 'author', 'owner')


class BookDetailView(DetailView):
    """Детали книги + счётчик просмотров."""

    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get_queryset(self):
        """Оптимизирует запрос."""
        return Book.objects.select_related('genre', 'author', 'owner')

    def get(self, request, *args, **kwargs):
        """Увеличивает счётчик просмотров для всех, кроме владельца."""
        response = super().get(request, *args, **kwargs)
        book = self.object
        user = request.user

        # Не считаем просмотр владельца и админа
        is_owner = user.is_authenticated and book.owner_id == user.id
        is_admin = user.is_authenticated and user.is_staff

        if not is_owner and not is_admin:
            book.views += 1
            book.save(update_fields=['views'])
            if book.views % 20 == 0:
                send_views_milestone_email(book)

        return response


class BookCreateView(AuthorRequiredMixin, CreateView):
    """Создание книги."""

    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('books:book_list')

    def get_context_data(self, **kwargs):
        """Добавляет action в контекст."""
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Создать'
        return ctx

    def form_valid(self, form):
        """Привязывает книгу к пользователю и шлёт письмо."""
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        logger.info('User %s created book "%s"', self.request.user, self.object.title)
        send_new_book_email(self.object)
        return response


class BookUpdateView(IsOwnerOrModeratorMixin, UpdateView):
    """Редактирование книги.

    - Владелец — видит только базовые поля.
    - Модератор/админ — видит все поля (включая is_active, owner, views).
    """

    model = Book
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('books:book_list')

    def get_form_class(self):
        """Выбирает форму в зависимости от роли."""
        if self.request.user.is_moderator:
            return BookAdminUpdateForm
        return BookUpdateForm

    def get_context_data(self, **kwargs):
        """Добавляет action."""
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Обновить'
        return ctx

    def form_valid(self, form):
        """Логирует обновление."""
        logger.info(
            'User %s updated book "%s"',
            self.request.user, self.object.title,
        )
        return super().form_valid(form)


class BookDeleteView(IsOwnerOrModeratorMixin, DeleteView):
    """Удаление книги."""

    model = Book
    template_name = 'books/book_confirm_delete.html'
    success_url = reverse_lazy('books:book_list')

    def form_valid(self, form):
        """Логирует удаление."""
        logger.info(
            'User %s deleted book "%s"',
            self.request.user, self.object.title,
        )
        return super().form_valid(form)


class BookToggleActiveView(ModeratorRequiredMixin, UpdateView):
    """Быстрая смена активности книги (только модератор/админ)."""

    model = Book
    fields = []
    template_name = 'books/book_toggle_confirm.html'
    success_url = reverse_lazy('books:book_list')

    def form_valid(self, form):
        """Переключает is_active."""
        self.object.is_active = not self.object.is_active
        self.object.save(update_fields=['is_active'])
        logger.info(
            'User %s toggled active for book "%s" → %s',
            self.request.user, self.object.title, self.object.is_active,
        )
        return super().form_valid(form)
# ============ GENRE ============

class GenreListView(ListView):
    """Список жанров."""

    model = Genre
    template_name = 'books/genre_list.html'
    context_object_name = 'genres'


class GenreDetailView(DetailView):
    """Детали жанра."""

    model = Genre
    template_name = 'books/genre_detail.html'
    context_object_name = 'genre'


class GenreCreateView(AuthorRequiredMixin, CreateView):
    """Создание жанра."""

    model = Genre
    form_class = GenreForm
    template_name = 'books/genre_form.html'
    success_url = reverse_lazy('books:genre_list')

    def get_context_data(self, **kwargs):
        """Добавляет action."""
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Создать'
        return ctx


class GenreUpdateView(AuthorRequiredMixin, UpdateView):
    """Редактирование жанра."""

    model = Genre
    form_class = GenreForm
    template_name = 'books/genre_form.html'
    success_url = reverse_lazy('books:genre_list')

    def get_context_data(self, **kwargs):
        """Добавляет action."""
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Обновить'
        return ctx


class GenreDeleteView(AuthorRequiredMixin, DeleteView):
    """Удаление жанра."""

    model = Genre
    template_name = 'books/genre_confirm_delete.html'
    success_url = reverse_lazy('books:genre_list')


# ============ AUTHOR (родословная) ============

class AuthorListView(ListView):
    """Список авторов."""

    model = Author
    template_name = 'books/author_list.html'
    context_object_name = 'authors'
    paginate_by = 10


class AuthorDetailView(DetailView):
    """Детали автора с его книгами."""

    model = Author
    template_name = 'books/author_detail.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        """Добавляет список книг автора."""
        ctx = super().get_context_data(**kwargs)
        ctx['books'] = self.object.books.select_related('genre', 'owner')
        return ctx


class AuthorCreateView(AuthorRequiredMixin, CreateView):
    """Создание автора."""

    model = Author
    form_class = AuthorForm
    template_name = 'books/author_form.html'
    success_url = reverse_lazy('books:author_list')

    def get_context_data(self, **kwargs):
        """Добавляет action."""
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Создать'
        return ctx


class AuthorUpdateView(AuthorRequiredMixin, UpdateView):
    """Редактирование автора."""

    model = Author
    form_class = AuthorForm
    template_name = 'books/author_form.html'
    success_url = reverse_lazy('books:author_list')

    def get_context_data(self, **kwargs):
        """Добавляет action."""
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Обновить'
        return ctx


class AuthorDeleteView(AuthorRequiredMixin, DeleteView):
    """Удаление автора."""

    model = Author
    template_name = 'books/author_confirm_delete.html'
    success_url = reverse_lazy('books:author_list')


# ============ REVIEWS ============

class ReviewCreateView(LoginRequiredMixin, CreateView):
    """Создание отзыва на книгу."""

    model = Review
    form_class = ReviewForm
    template_name = 'books/review_form.html'

    def dispatch(self, request, *args, **kwargs):
        """Сохраняет book_id из URL."""
        self.book = get_object_or_404(Book, pk=kwargs['book_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Привязывает отзыв к книге и пользователю."""
        form.instance.book = self.book
        form.instance.user = self.request.user
        logger.info(
            'User %s created review for book "%s"',
            self.request.user, self.book.title,
        )
        return super().form_valid(form)

    def get_success_url(self):
        """Возвращает на страницу книги."""
        return reverse_lazy('books:book_detail', kwargs={'pk': self.book.pk})

    def get_context_data(self, **kwargs):
        """Добавляет книгу в контекст."""
        ctx = super().get_context_data(**kwargs)
        ctx['book'] = self.book
        return ctx


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование отзыва (только автор)."""

    model = Review
    form_class = ReviewForm
    template_name = 'books/review_form.html'

    def dispatch(self, request, *args, **kwargs):
        """Проверяет, что отзыв принадлежит пользователю."""
        review = self.get_object()
        if review.user != request.user and not request.user.is_staff:
            raise PermissionDenied('Вы можете редактировать только свои отзывы.')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """Возвращает на страницу книги."""
        return reverse_lazy('books:book_detail', kwargs={'pk': self.object.book.pk})

    def get_context_data(self, **kwargs):
        """Добавляет книгу."""
        ctx = super().get_context_data(**kwargs)
        ctx['book'] = self.object.book
        return ctx


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление отзыва (только автор или админ)."""

    model = Review
    template_name = 'books/review_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        """Проверяет права."""
        review = self.get_object()
        if review.user != request.user and not request.user.is_staff:
            raise PermissionDenied('Вы можете удалять только свои отзывы.')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """Возвращает на страницу книги."""
        return reverse_lazy('books:book_detail', kwargs={'pk': self.object.book.pk})
