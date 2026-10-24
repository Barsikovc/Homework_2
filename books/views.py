"""Views для приложения books (CBV)."""
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)

from .forms import AuthorForm, BookForm, GenreForm
from .mixins import AuthorRequiredMixin, IsOwnerOrModeratorMixin
from .models import Author, Book, Genre
from .services import send_new_book_email

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
    """Детали книги."""

    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get_queryset(self):
        """Оптимизирует запрос."""
        return Book.objects.select_related('genre', 'author', 'owner')


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
    """Редактирование книги."""

    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('books:book_list')

    def get_context_data(self, **kwargs):
        """Добавляет action в контекст."""
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
