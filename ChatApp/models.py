from django.db import models
from django.contrib.auth.models import User

class ChatGroup(models.Model):
    name = models.CharField(max_length=100, default=User)
    description = models.TextField(default="ChatGroup")
    members = models.ManyToManyField(User)

    def __str__(self) -> str:
        return self.name

class Message(models.Model):
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} ({self.timestamp}): {self.text}'

class Reaction(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emoji = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user} reacted to "{self.message.text}" with {self.emoji}'

