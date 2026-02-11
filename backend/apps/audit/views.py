from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.organizations.models import Membership
from .models import AuditLog
from .serializers import AuditLogSerializer


class AuditLogListView(generics.ListAPIView):
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        memberships = Membership.objects.filter(user=self.request.user)
        return AuditLog.objects.filter(organization_id__in=memberships.values_list("organization_id", flat=True))
