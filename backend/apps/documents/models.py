from django.conf import settings
from django.db import models

from apps.organizations.models import Organization


class Document(models.Model):
    class Status(models.TextChoices):
        UPLOADED = "uploaded", "Uploaded"
        PARSING = "parsing", "Parsing"
        CHUNKING = "chunking", "Chunking"
        EMBEDDING = "embedding", "Embedding"
        READY = "ready", "Ready"
        FAILED = "failed", "Failed"

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="documents")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="documents")
    file = models.FileField(upload_to="documents/")
    name = models.CharField(max_length=255)
    content_type = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UPLOADED)
    extracted_text = models.TextField(blank=True, default="")
    extracted_tables = models.JSONField(default=list, blank=True)
    error_message = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DocumentChunk(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="chunks")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="document_chunks")
    chunk_index = models.PositiveIntegerField()
    text = models.TextField()
    snippet = models.CharField(max_length=500)
    metadata = models.JSONField(default=dict, blank=True)
    embedding = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("document", "chunk_index")
