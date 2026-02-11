from apps.organizations.models import Organization
from .models import AuditLog


def log_action(actor, organization: Organization | None, action: str, target_type: str, target_id: str, metadata=None):
    AuditLog.objects.create(
        actor=actor if getattr(actor, "is_authenticated", False) else None,
        organization=organization,
        action=action,
        target_type=target_type,
        target_id=target_id,
        metadata=metadata or {},
    )
