from django.shortcuts import render
from .models import Message


def message_history(request):
    messages = Message.objects.all()
    return render(request, 'history.html', {'messages': messages})
