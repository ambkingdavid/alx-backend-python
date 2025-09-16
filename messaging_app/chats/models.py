from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    user_id: uuid.UUID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # type: ignore
    email: str = models.EmailField(unique=True) # type: ignore
    password_hash: str = models.CharField(max_length=128) # type: ignore
    phone_number: str = models.CharField(max_length=20, null=True, blank=True) # type: ignore

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role: str = models.CharField(max_length=10, choices=ROLE_CHOICES) # type: ignore
    created_at = models.DateTimeField(auto_now_add=True) # type: ignore

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.email} ({self.role})"


class Conversation(models.Model):
    conversation_id: uuid.UUID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # type: ignore
    participants = models.ManyToManyField(User, related_name='conversations') # type: ignore
    created_at = models.DateTimeField(auto_now_add=True) # type: ignore

    def __str__(self):
        return f"Conversation {self.conversation_id}"

class Message(models.Model):
    message_id: uuid.UUID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # type: ignore
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages') # type: ignore
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages') # type: ignore
    message_body = models.TextField() # type: ignore
    sent_at = models.DateTimeField(auto_now_add=True) # type: ignore

    def __str__(self):
        return f"Message from {self.sender.email} at {self.sent_at}" # type: ignore
