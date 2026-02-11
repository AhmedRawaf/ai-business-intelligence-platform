from django.urls import path
from .views import KPIAnalyticsView, KPIDataSetListCreateView

urlpatterns = [
    path("datasets", KPIDataSetListCreateView.as_view()),
    path("analytics", KPIAnalyticsView.as_view()),
]
