from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.audit.services import log_action
from apps.organizations.models import Membership
from .models import Document
from .serializers import DocumentSerializer
from .tasks import parse_document


class DocumentListCreateView(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        memberships = Membership.objects.filter(user=self.request.user)
        org_ids = memberships.values_list("organization_id", flat=True)
        queryset = Document.objects.filter(organization_id__in=org_ids).select_related("organization", "uploaded_by")
        organization_id = self.request.query_params.get("organization")
        if organization_id:
            queryset = queryset.filter(organization_id=organization_id)
        return queryset.order_by("-created_at")

    def perform_create(self, serializer):
        document = serializer.save(uploaded_by=self.request.user, name=serializer.validated_data["file"].name)
        log_action(
            actor=self.request.user,
            organization=document.organization,
            action="document_uploaded",
            target_type="document",
            target_id=str(document.id),
            metadata={"file": document.name},
        )
        parse_document.delay(document.id)
