from __future__ import annotations
from django.shortcuts import render # type: ignore

from typing import Any

from django.shortcuts import get_object_or_404
from django.db.models import QuerySet
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet[Conversation]):
    """
    ViewSet for listing, retrieving, and creating conversations.
    """
    queryset: QuerySet[Conversation] = Conversation.objects.all() # type: ignore
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Create a new conversation with participants.
        Expected payload:
        {
            "participants": [<user_id>, <user_id>, ...]
        }
        """
        participant_ids: list[str] = request.data.get("participants", [])
        if not participant_ids:
            return Response(
                {"error": "Participants list is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        participants: QuerySet[User] = User.objects.filter(user_id__in=participant_ids)
        if not participants.exists():
            return Response(
                {"error": "No valid participants found."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation: Conversation = Conversation.objects.create()
        conversation.participants.set(participants) # type: ignore
        conversation.save()

        serializer: ConversationSerializer = self.get_serializer(conversation) # type: ignore
        return Response(serializer.data, status=status.HTTP_201_CREATED) # type: ignore


class MessageViewSet(viewsets.ModelViewSet[Message]):
    """
    ViewSet for listing, retrieving, and sending messages.
    """
    queryset: QuerySet[Message] = Message.objects.all() # type: ignore
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Send a message to an existing conversation.
        Expected payload:
        {
            "conversation_id": "<uuid>",
            "message_body": "Hello there!"
        }
        """
        conversation_id: str | None = request.data.get("conversation_id")
        message_body: str | None = request.data.get("message_body")

        if not conversation_id or not message_body:
            return Response(
                {"error": "conversation_id and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation: Conversation = get_object_or_404(
            Conversation, conversation_id=conversation_id
        )

        message: Message = Message.objects.create(
            sender=request.user,  # type: ignore[arg-type]
            conversation=conversation,
            message_body=message_body
        )

        serializer: MessageSerializer = self.get_serializer(message) # type: ignore
        return Response(serializer.data, status=status.HTTP_201_CREATED) # type: ignore

