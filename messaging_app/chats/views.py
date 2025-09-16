from __future__ import annotations
from typing import Any

from django.shortcuts import get_object_or_404
from django.db.models import QuerySet
from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet[Conversation]):
    queryset: QuerySet[Conversation] = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]  # ✅ Added filter backend
    search_fields = ['participants__email']   # Example filter

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        participant_ids: list[str] = request.data.get("participants", [])
        if not participant_ids:
            return Response({"error": "Participants list is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        participants = User.objects.filter(user_id__in=participant_ids)
        if not participants.exists():
            return Response({"error": "No valid participants found."},
                            status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet[Message]):
    queryset: QuerySet[Message] = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]  # ✅ Added filter backend
    search_fields = ['message_body', 'sender__email']  # Example filter

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        conversation_id: str | None = request.data.get("conversation_id")
        message_body: str | None = request.data.get("message_body")

        if not conversation_id or not message_body:
            return Response({"error": "conversation_id and message_body are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)

        message = Message.objects.create(
            sender=request.user,  # type: ignore[arg-type]
            conversation=conversation,
            message_body=message_body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
