from django.conf import settings
from django.db import models

from apps.organizations.models import Organization


class KPIDataSet(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="kpi_datasets")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="kpi_datasets")
    name = models.CharField(max_length=255)
    source_file = models.FileField(upload_to="kpi/")
    columns = models.JSONField(default=list, blank=True)
    row_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class KPIRecord(models.Model):
    dataset = models.ForeignKey(KPIDataSet, on_delete=models.CASCADE, related_name="records")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="kpi_records")
    data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
