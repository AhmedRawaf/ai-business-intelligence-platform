from django.urls import path
from .views import ChatAskView, ChatSessionListCreateView

urlpatterns = [
    path("sessions", ChatSessionListCreateView.as_view()),
    path("ask", ChatAskView.as_view()),
]
