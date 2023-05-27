from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import Thread, ChatMessage
admin.site.register(ChatMessage)


class ChatMessage(admin.TabularInline):
    model = ChatMessage
    ChatMessage.user


class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    class Meta:
        model = Thread
print('hey')

admin.site.register(Thread, ThreadAdmin)

