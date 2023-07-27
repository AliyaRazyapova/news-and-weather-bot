from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render
from .models import Message


def message_history(request):
    messages = Message.objects.all()
    return render(request, 'history.html', {'messages': messages})


@login_required
def dashboard(request):
    total_dialogs = Message.objects.count()
    total_user_messages = Message.objects.filter(is_bot=False).count()
    total_bot_responses = Message.objects.filter(is_bot=True).count()
    popular_commands = Message.objects.filter(is_bot=False, message__startswith='/').values('message').annotate(count=Count('message')).order_by('-count')[:5]

    context = {
        'total_dialogs': total_dialogs,
        'total_user_messages': total_user_messages,
        'total_bot_responses': total_bot_responses,
        'popular_commands': popular_commands,
    }

    return render(request, 'dashboard.html', context)
