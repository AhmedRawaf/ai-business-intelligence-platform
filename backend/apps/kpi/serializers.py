from rest_framework import serializers

from apps.organizations.models import Membership, Organization
from .models import KPIDataSet


class KPIDataSetSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())
    uploaded_by = serializers.CharField(source="uploaded_by.username", read_only=True)

    class Meta:
        model = KPIDataSet
        fields = (
            "id",
            "organization",
            "uploaded_by",
            "name",
            "source_file",
            "columns",
            "row_count",
            "created_at",
        )
        read_only_fields = ("columns", "row_count", "created_at")

    def validate_organization(self, value):
        user = self.context["request"].user
        if not Membership.objects.filter(user=user, organization=value).exists():
            raise serializers.ValidationError("Not allowed for this organization.")
        return value
