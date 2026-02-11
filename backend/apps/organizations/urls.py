from django.urls import path
from .views import MembershipListView, OrganizationListCreateView

urlpatterns = [
    path("", OrganizationListCreateView.as_view()),
    path("memberships", MembershipListView.as_view()),
]
