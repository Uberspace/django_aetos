import re

from django.http import HttpResponse
from django.shortcuts import render
from django_aetos import app_settings

from .signals import collect_metrics


def collect_response():
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

    return metrics


def check_auth(request):
    ip_address = request.META["REMOTE_ADDR"]
    allowed_ips = app_settings.IP_ALLOWLIST

    if app_settings.ENABLE_IP_ALLOWLIST and ip_address in allowed_ips:
        return True
    elif not app_settings.ENABLE_IP_ALLOWLIST:
        return True
    else:
        return False


def check_ips(request):
    try:
        authorization_header = request.META["HTTP_AUTHORIZATION"]
    except KeyError:
        authorization_header = ""
    type, sep, token = authorization_header.partition(" ")
    allowed_tokens = app_settings.AUTH_TOKENLIST

    if app_settings.ENABLE_AUTH and type == "Bearer" and token in allowed_tokens:
        return True
    elif not app_settings.ENABLE_AUTH:
        return True
    else:
        return False


def export_metrics(request):
    if check_auth(request) and check_ips(request):
        response = render(
            request,
            "metrics/export.txt",
            context={"metrics": collect_response()},
            content_type="text/plain",
        )
        response.content = re.sub(b"\n+", b"\n", response.content)

        return response
    else:
        return HttpResponse(status=401)
