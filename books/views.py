"""Views для приложения books (FBV)."""
from django.contrib.auth.decorators import login_required
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
    return render(request, 'books/book_form.html', {'form': form})


def genre_list(request):
    """Отображает список всех жанров."""
    genres = Genre.objects.all()
    return render(request, 'books/genre_list.html', {'genres': genres})
