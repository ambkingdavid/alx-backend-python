from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer): # type: ignore
    role = serializers.CharField(read_only=True) 

    class Meta: # type: ignore
        model = User
        fields = [
            'user_id', 'first_name', 'last_name',
            'email', 'phone_number', 'role', 'created_at'
        ]


class MessageSerializer(serializers.ModelSerializer): # type: ignore
    sender = UserSerializer(read_only=True)

    class Meta: # type: ignore
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']

    def validate_message_body(self, value): # type: ignore
        """Ensure message body is not empty."""
        if not value.strip(): # type: ignore
            raise serializers.ValidationError("Message body cannot be empty.")
        return value # type: ignore


class ConversationSerializer(serializers.ModelSerializer): # type: ignore
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField() # type: ignore

    class Meta: # type: ignore
        model = Conversation
        fields = [
            'conversation_id', 'participants',
            'created_at', 'messages', 'message_count'
        ]

    def get_message_count(self, obj): # type: ignore
        """Return the number of messages in this conversation."""
        return obj.messages.count() # type: ignore

