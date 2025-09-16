from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta: # type: ignore
        model = User
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'created_at',
        ]

class MessageSerializer(serializers.ModelSerializer[Message]):
    sender = UserSerializer(read_only=True)

    class Meta: # type: ignore
        model = Message
        fields = [
            'message_id',
            'sender',
            'message_body',
            'sent_at',
        ]

class ConversationSerializer(serializers.ModelSerializer[Conversation]):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta: # type: ignore
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'created_at',
            'messages',
        ]
