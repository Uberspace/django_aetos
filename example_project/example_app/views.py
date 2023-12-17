from django.http import HttpResponse

from .models import Book


def list_books(request):
    return HttpResponse("\n".join(f"{b.title} by {b.author}" for b in Book.objects.all()))
