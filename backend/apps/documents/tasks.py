from celery import shared_task

from apps.ai.providers import EmbeddingProvider
from apps.audit.services import log_action
from .chunking import chunk_text
from .models import Document, DocumentChunk
from .parsers import parse_document_file


@shared_task
def parse_document(document_id: int):
    document = Document.objects.get(id=document_id)
    document.status = Document.Status.PARSING
    document.save(update_fields=["status", "updated_at"])
    try:
        text, tables = parse_document_file(document.file.path)
        document.extracted_text = text
        document.extracted_tables = tables
        document.status = Document.Status.CHUNKING
        document.save(update_fields=["extracted_text", "extracted_tables", "status", "updated_at"])
        chunk_document.delay(document.id)
    except Exception as exc:  # noqa: BLE001
        document.status = Document.Status.FAILED
        document.error_message = str(exc)
        document.save(update_fields=["status", "error_message", "updated_at"])


@shared_task
def chunk_document(document_id: int):
    document = Document.objects.get(id=document_id)
    document.status = Document.Status.CHUNKING
    document.save(update_fields=["status", "updated_at"])
    try:
        DocumentChunk.objects.filter(document=document).delete()
        chunks = chunk_text(document.extracted_text)
        for idx, text in enumerate(chunks):
            DocumentChunk.objects.create(
                document=document,
                organization=document.organization,
                chunk_index=idx,
                text=text,
                snippet=text[:450],
                metadata={},
            )
        document.status = Document.Status.EMBEDDING
        document.save(update_fields=["status", "updated_at"])
        embed_document.delay(document.id)
    except Exception as exc:  # noqa: BLE001
        document.status = Document.Status.FAILED
        document.error_message = str(exc)
        document.save(update_fields=["status", "error_message", "updated_at"])


@shared_task
def embed_document(document_id: int):
    document = Document.objects.get(id=document_id)
    document.status = Document.Status.EMBEDDING
    document.save(update_fields=["status", "updated_at"])
    embedder = EmbeddingProvider()
    try:
        for chunk in document.chunks.all():
            chunk.embedding = embedder.embed(chunk.text)
            chunk.save(update_fields=["embedding"])
        document.status = Document.Status.READY
        document.save(update_fields=["status", "updated_at"])
        log_action(
            actor=document.uploaded_by,
            organization=document.organization,
            action="document_processed",
            target_type="document",
            target_id=str(document.id),
            metadata={"name": document.name, "status": document.status},
        )
    except Exception as exc:  # noqa: BLE001
        document.status = Document.Status.FAILED
        document.error_message = str(exc)
        document.save(update_fields=["status", "error_message", "updated_at"])
