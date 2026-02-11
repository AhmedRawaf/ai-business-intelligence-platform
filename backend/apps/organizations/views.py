from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.utils.text import slugify

from .models import Membership, Organization
from .serializers import MembershipSerializer, OrganizationSerializer


class OrganizationListCreateView(generics.ListCreateAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        memberships = Membership.objects.filter(user=self.request.user).select_related("organization")
        org_ids = [membership.organization_id for membership in memberships]
        return Organization.objects.filter(id__in=org_ids).order_by("name")

    def perform_create(self, serializer):
        organization = serializer.save(slug=slugify(serializer.validated_data["name"]))
        Membership.objects.create(
            user=self.request.user,
            organization=organization,
            role=Membership.Roles.ADMIN,
        )


class MembershipListView(generics.ListAPIView):
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Membership.objects.filter(user=self.request.user).select_related("organization")
