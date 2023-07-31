from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Message, BotResponse


def message_history(request):
    messages = Message.objects.all()
    return render(request, 'history.html', {'messages': messages})


from django.http import Http404

def user_message_history(request):
    user_id = request.GET.get('user_id')
    if user_id is None:
        raise Http404("User ID not specified in the URL")

    messages = Message.objects.filter(user_id=user_id)
    return render(request, 'user_history.html', {'messages': messages})


def message_list_json(request):
    messages = Message.objects.all().values('timestamp', 'message')
    return JsonResponse(list(messages), safe=False)


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


def bot_response_list(request):
    templates = BotResponse.objects.all()
    return render(request, 'response_list.html', {'templates': templates})


def bot_response_edit(request, template_id):
    template = get_object_or_404(BotResponse, pk=template_id)
    if request.method == 'POST':
        template.command == request.POST['command']
        template.response == request.POST['response']
        template.save()
        return redirect('response_list.html')
    return render(request, 'response_form.html', {'template': template})
