from django.urls import path

from .views import export_metrics
from .views import export_metrics_by_category

app_name = "metrics"
urlpatterns = [
    path("metrics/<str:category>", export_metrics_by_category, name="metrics_by_category"),
    path("metrics", export_metrics, name="metrics"),
]
