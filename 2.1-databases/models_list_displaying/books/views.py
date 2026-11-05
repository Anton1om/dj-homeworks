from datetime import datetime

from django.shortcuts import render, redirect
from django.http import Http404

from books.models import Book


def index(request):
    return redirect('books')


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()
    context = {'books': books}
    return render(request, template, context)


def books_by_date_view(request, date):
    try:
        parsed_date = datetime.strptime(date, '%Y-%m-%d').date()
    except Exception:
        raise Http404(f"Неверный формат даты: {date}. Ожидается YYYY-MM-DD")

    template = 'books/books_by_date.html'
    books = Book.objects.filter(pub_date=parsed_date)

    prev_date = (
        Book.objects.filter(pub_date__lt=parsed_date)
        .order_by('-pub_date').values_list('pub_date', flat=True).first()
    )
    next_date = (
        Book.objects.filter(pub_date__gt=parsed_date)
        .order_by('pub_date').values_list('pub_date', flat=True).first()
    )

    context = {
        'books': books,
        'prev_date': prev_date,
        'next_date': next_date
    }
    return render(request, template, context)