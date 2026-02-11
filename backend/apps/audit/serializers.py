from rest_framework import serializers
from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    actor_name = serializers.SerializerMethodField()
    organization_name = serializers.SerializerMethodField()

    class Meta:
        model = AuditLog
        fields = (
            "id",
            "actor_name",
            "organization_name",
            "action",
            "target_type",
            "target_id",
            "metadata",
            "created_at",
        )

    def get_actor_name(self, obj):
        if not obj.actor:
            return "System"
        return obj.actor.username

    def get_organization_name(self, obj):
        return obj.organization.name if obj.organization else None
