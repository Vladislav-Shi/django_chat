from django.contrib import admin
from .models import ChatModel, MessageModel, ChatUser

admin.site.register(ChatModel)
admin.site.register(MessageModel)
admin.site.register(ChatUser)
