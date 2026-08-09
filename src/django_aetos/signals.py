from collections import defaultdict
from functools import wraps

import django.dispatch
from django.dispatch import receiver

collect_metrics = django.dispatch.Signal()

_metric_collectors = defaultdict(list)


def metric_collector(category):
    def decorator(func):
        _metric_collectors[category].append(func)

        @receiver(collect_metrics, dispatch_uid=f"{category}:{func.__module__}.{func.__name__}")
        @wraps(func)
        def wrapper(sender, **kwargs):
            return func(sender, **kwargs)

        return wrapper

    return decorator


def get_collectors_by_category(category):
    return _metric_collectors.get(category, [])
