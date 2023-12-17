from django.urls import path

from .views import export_metrics

app_name = "metrics"
urlpatterns = [
    path("metrics", export_metrics),
]
