from rest_framework import viewsets, mixins, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from typing import cast, Optional

class ConversationViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing conversations.
    """
    queryset = Conversation.objects.all().order_by('-created_at')
    serializer_class = ConversationSerializer

    @action(detail=True, methods=['post'])
    def send_message(self, request: Request, pk: Optional[str] = None) -> Response:
        """
        Send a new message to an existing conversation.
        """
        try:
            conversation: Conversation = self.get_object()
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)

        # Use 'cast' to tell mypy that request.user is an instance of your User model
        sender: User = cast(User, request.user)
        
        # Check if the user is a participant in the conversation
        if not conversation.participants.filter(pk=sender.pk).exists(): # type: ignore
            return Response({'error': 'You are not a participant in this conversation'}, status=status.HTTP_403_FORBIDDEN)

        message_body: str = request.data.get('message_body', '')
        if not message_body:
            return Response({'error': 'Message body is required'}, status=status.HTTP_400_BAD_REQUEST)

        message: Message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body
        )
        serializer: MessageSerializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """
    A viewset for listing and retrieving messages.
    """
    queryset = Message.objects.all().order_by('-sent_at')
    serializer_class = MessageSerializer
