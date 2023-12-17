from django.dispatch import receiver
from django_aetos.signals import collect_metrics

from .models import Book


@receiver(collect_metrics, dispatch_uid="metric_books_count")
def metric_books_count(sender, **kwargs):
    yield {
        "name": "books_count",
        "help": "Total number of books",
        "type": "counter",
        "value": Book.objects.count(),
    }


@receiver(collect_metrics, dispatch_uid="metric_universes_count")
def metric_universes_count(sender, **kwargs):
    yield {
        "name": "universes_count",
        "help": "Total number of universes",
        "type": "counter",
        "value": "1",
    }
