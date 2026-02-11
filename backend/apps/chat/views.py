import hashlib

from django.core.cache import cache
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ai.providers import ChatProvider, EmbeddingProvider
from apps.ai.retrieval import build_citations, retrieve_top_chunks
from apps.audit.services import log_action
from apps.common.rate_limit import check_rate_limit
from apps.organizations.models import Membership
from .models import ChatMessage, ChatSession
from .serializers import ChatAskSerializer, ChatSessionSerializer


class ChatSessionListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        memberships = Membership.objects.filter(user=self.request.user)
        org_ids = memberships.values_list("organization_id", flat=True)
        queryset = ChatSession.objects.filter(organization_id__in=org_ids, user=self.request.user)
        organization_id = self.request.query_params.get("organization")
        if organization_id:
            queryset = queryset.filter(organization_id=organization_id)
        return queryset.order_by("-updated_at")

    def perform_create(self, serializer):
        organization = serializer.validated_data["organization"]
        if not Membership.objects.filter(user=self.request.user, organization=organization).exists():
            raise PermissionDenied("Not allowed.")
        serializer.save(user=self.request.user)


class ChatAskView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        check_rate_limit(f"chat:{request.user.id}", limit=25, window_seconds=60)
        serializer = ChatAskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        organization = serializer.validated_data["organization"]
        if not Membership.objects.filter(user=request.user, organization=organization).exists():
            return Response({"detail": "Not allowed for this organization."}, status=status.HTTP_403_FORBIDDEN)

        question = serializer.validated_data["question"]
        language = serializer.validated_data["language"]
        session_id = serializer.validated_data.get("session_id")

        if session_id:
            session = ChatSession.objects.filter(id=session_id, user=request.user, organization=organization).first()
            if not session:
                return Response({"detail": "Session not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            session = ChatSession.objects.create(user=request.user, organization=organization, title=question[:80])

        ChatMessage.objects.create(session=session, role=ChatMessage.Role.USER, content=question)

        cache_key = f"rag:{organization.id}:{hashlib.sha256(question.encode('utf-8')).hexdigest()}"
        cached = cache.get(cache_key)
        if cached:
            answer = cached["answer"]
            citations = cached["citations"]
        else:
            embedder = EmbeddingProvider()
            query_embedding = embedder.embed(question)
            chunks = retrieve_top_chunks(organization.id, query_embedding, top_k=5)
            contexts = [chunk.text for chunk in chunks]
            answer = ChatProvider().answer(query=question, contexts=contexts, language=language)
            citations = build_citations(chunks)
            cache.set(cache_key, {"answer": answer, "citations": citations}, timeout=600)

        assistant_message = ChatMessage.objects.create(
            session=session,
            role=ChatMessage.Role.ASSISTANT,
            content=answer,
            citations=citations,
        )

        log_action(
            actor=request.user,
            organization=organization,
            action="ai_query",
            target_type="chat_session",
            target_id=str(session.id),
            metadata={"question": question, "message_id": assistant_message.id},
        )

        return Response(
            {
                "session_id": session.id,
                "answer": answer,
                "citations": citations,
            }
        )
