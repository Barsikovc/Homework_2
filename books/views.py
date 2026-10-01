"""Views для приложения books (FBV)."""
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookForm
from .models import Book, Genre


def book_list(request):
    """Отображает список всех книг."""
    books = Book.objects.select_related('genre', 'owner').all()
    return render(request, 'books/book_list.html', {'books': books})


def book_detail(request, pk):
    """Отображает одну книгу."""
    book = get_object_or_404(Book.objects.select_related('genre', 'owner'), pk=pk)
    return render(request, 'books/book_detail.html', {'book': book})


@login_required
def book_create(request):
    """Создаёт новую книгу."""
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()
            return redirect('books:book_detail', pk=book.pk)
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form, 'action': 'Создать'})


@login_required
def book_update(request, pk):
    """Редактирует существующую книгу.

    Доступ: только владелец или админ.
    """
    book = get_object_or_404(Book, pk=pk)

    if book.owner != request.user and not request.user.is_staff:
        raise PermissionDenied('Вы не можете редактировать чужую книгу.')

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('books:book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form, 'action': 'Обновить'})


@login_required
def book_delete(request, pk):
    """Удаляет книгу.

    Доступ: только владелец или админ.
    """
    book = get_object_or_404(Book, pk=pk)

    if book.owner != request.user and not request.user.is_staff:
        raise PermissionDenied('Вы не можете удалить чужую книгу.')

    if request.method == 'POST':
        book.delete()
        return redirect('books:book_list')
    return render(request, 'books/book_delete.html', {'book': book})


def genre_list(request):
    """Отображает список всех жанров."""
    genres = Genre.objects.all()
    return render(request, 'books/genre_list.html', {'genres': genres})
