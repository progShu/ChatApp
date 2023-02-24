from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Message, ChatGroup


class UpdateForm(UserChangeForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username","email", "first_name"]


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["message"]

class CreateGroupForm(forms.ModelForm):
    name = forms.CharField(required=True)

    class Meta:
        model = ChatGroup
        fields = ["name"]