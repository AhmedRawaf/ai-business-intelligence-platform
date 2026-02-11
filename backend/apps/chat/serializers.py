from rest_framework import serializers

from apps.organizations.models import Organization
from .models import ChatMessage, ChatSession


class ChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = ("id", "organization", "title", "created_at", "updated_at")


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ("id", "session", "role", "content", "citations", "created_at")


class ChatAskSerializer(serializers.Serializer):
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())
    session_id = serializers.IntegerField(required=False)
    question = serializers.CharField()
    language = serializers.ChoiceField(choices=["ar", "en"], default="ar")
