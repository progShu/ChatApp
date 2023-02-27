from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Message, ChatGroup, Reaction


class UpdateForm(UserChangeForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username","email", "first_name"]

class ChatGroupForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = ['name', 'description', 'members']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["text"]

class ReactionForm(forms.ModelForm):
    class Meta:
        model = Reaction
        fields = ['emoji']
