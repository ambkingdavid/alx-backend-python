from rest_framework import serializers
from .models import User, Conversation, Message
from typing import Any, Dict

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'role']

class MessageSerializer(serializers.ModelSerializer):
    sender: serializers.Serializer = serializers.StringRelatedField() # type: ignore

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at']
        read_only_fields = ['sent_at', 'message_id']

class ConversationSerializer(serializers.ModelSerializer):
    participants: serializers.Serializer = UserSerializer(many=True, read_only=True) # type: ignore
    messages: serializers.Serializer = MessageSerializer(many=True, read_only=True) # type: ignore

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']
        read_only_fields = ['conversation_id', 'created_at']
