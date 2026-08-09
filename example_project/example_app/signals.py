from django.dispatch import receiver
from django_aetos.signals import collect_metrics
from django_aetos.signals import metric_collector

from .models import Book


@metric_collector(category="cheap")
def metric_books_count(sender, **kwargs):
    yield {
        "name": "books_count",
        "help": "Total number of books",
        "type": "counter",
        "value": Book.objects.count(),
    }


@metric_collector(category="cheap")
def metric_universes_count(sender, **kwargs):
    yield {
        "name": "universes_count",
        "help": "Total number of universes",
        "type": "counter",
        "value": "1",
    }


@receiver(collect_metrics, dispatch_uid="metric_legacy_example")
def metric_legacy_example(sender, **kwargs):
    yield {
        "name": "legacy_metric",
        "help": "Example of legacy receiver pattern still working",
        "type": "gauge",
        "value": "42",
    }
