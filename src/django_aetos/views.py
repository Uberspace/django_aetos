import re

from django.shortcuts import render

from .signals import collect_metrics


def export_metrics(request):
    metrics = []
    known_metrics = set()

    for _, signal_metrics in collect_metrics.send(None):
        for metric in signal_metrics:
            assert metric.keys() == {"name", "help", "type", "value"}
            metric = metric.copy()
            metric["name_without_labels"] = metric["name"].partition("{")[0]
            if metric["name_without_labels"] not in known_metrics:
                metric["add_help"] = True
            known_metrics.add(metric["name_without_labels"])
            metrics.append(metric)

    response = render(
        request,
        "metrics/export.txt",
        context={"metrics": metrics},
        content_type="text/plain",
    )
    response.content = re.sub(b"\n+", b"\n", response.content)
    return response
