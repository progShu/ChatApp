from django.contrib import admin
from .models import Message, ChatGroup, Reaction
# Register your models here.

admin.site.register(ChatGroup)
admin.site.register(Message)
admin.site.register(Reaction)
