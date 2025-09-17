import uuid
from typing import TYPE_CHECKING, cast
from django.db import models
from django.contrib.auth.models import AbstractUser

if TYPE_CHECKING:
    from django.db.models import UUIDField, CharField, DateTimeField, ManyToManyField, ForeignKey, TextField

class User(AbstractUser):
    """
    Extends the built-in Django User model to add custom fields.
    """
    # Corrected type hint: Use `models.UUIDField` for the annotation
    user_id: models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    phone_number: models.CharField = models.CharField(max_length=15, null=True, blank=True)
    ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    )
    role: models.CharField = models.CharField(max_length=5, choices=ROLE_CHOICES, default='guest')
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.username

class Conversation(models.Model):
    """
    Represents a conversation between two or more users.
    """
    conversation_id: models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    participants: models.ManyToManyField = models.ManyToManyField(User, related_name='conversations')  # type: ignore
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Conversation {self.conversation_id}"

class Message(models.Model):
    """
    Represents a single message within a conversation.
    """
    message_id: models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    conversation: models.ForeignKey = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message_body: models.TextField = models.TextField()
    sent_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        # Use cast to inform mypy that self.sender is a User object
        sender_user = cast(User, self.sender)
        return f"Message from {sender_user.username} at {self.sent_at}"
