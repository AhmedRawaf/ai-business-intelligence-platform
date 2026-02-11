from django.conf import settings
from rest_framework import serializers

from apps.organizations.models import Membership, Organization
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())
    uploaded_by = serializers.CharField(source="uploaded_by.username", read_only=True)

    class Meta:
        model = Document
        fields = (
            "id",
            "organization",
            "uploaded_by",
            "name",
            "file",
            "content_type",
            "status",
            "error_message",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("status", "error_message", "created_at", "updated_at", "content_type")

    def validate_file(self, value):
        allowed = {
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/csv",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        }
        if value.content_type not in allowed:
            raise serializers.ValidationError("Unsupported file type.")
        if value.size > settings.MAX_UPLOAD_SIZE_BYTES:
            raise serializers.ValidationError("File too large.")
        return value

    def validate_organization(self, value):
        user = self.context["request"].user
        if not Membership.objects.filter(user=user, organization=value).exists():
            raise serializers.ValidationError("Not allowed for this organization.")
        return value

    def create(self, validated_data):
        uploaded = validated_data["file"]
        validated_data["content_type"] = uploaded.content_type
        return super().create(validated_data)
