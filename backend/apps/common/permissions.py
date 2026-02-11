from rest_framework.permissions import BasePermission
from apps.organizations.models import Membership


def get_membership(user, organization_id):
    return Membership.objects.filter(user=user, organization_id=organization_id).first()


class IsOrgMember(BasePermission):
    def has_permission(self, request, view):
        org_id = request.data.get("organization") or request.query_params.get("organization")
        if not org_id:
            return True
        return Membership.objects.filter(user=request.user, organization_id=org_id).exists()


class IsOrgManagerOrAbove(BasePermission):
    allowed_roles = {Membership.Roles.ADMIN, Membership.Roles.MANAGER}

    def has_permission(self, request, view):
        org_id = request.data.get("organization") or request.query_params.get("organization")
        if not org_id:
            return False
        membership = get_membership(request.user, org_id)
        return bool(membership and membership.role in self.allowed_roles)
