from django.contrib.auth.models import User
from rest_framework import serializers

from apps.organizations.models import Membership


class CurrentUserSerializer(serializers.ModelSerializer):
    memberships = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "memberships")

    def get_memberships(self, obj):
        memberships = Membership.objects.filter(user=obj).select_related("organization")
        return [
            {
                "organization_id": membership.organization_id,
                "organization_name": membership.organization.name,
                "role": membership.role,
            }
            for membership in memberships
        ]
