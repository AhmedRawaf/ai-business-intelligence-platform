from django.urls import path
from .views import CurrentUserView, LoginView, RefreshView

urlpatterns = [
    path("login", LoginView.as_view()),
    path("refresh", RefreshView.as_view()),
    path("me", CurrentUserView.as_view()),
]
