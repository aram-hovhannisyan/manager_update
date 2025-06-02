from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect

from .models import (
    Message, User
)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json


from django.utils import timezone

def create_announcement_view(request):
    customers = User.objects.filter(is_customer=True)
    customer_usernames = [i.username for i in customers]
    if request.method == 'POST':
        # Handle form submission

        message = request.POST.get('message')
        if message == "":
            return render(request, "messages/create_announcement_view.html", {
                "customers" : customer_usernames
            })
        selected_users = request.POST.getlist('selected_users')
        selected_users = ",".join(selected_users)
        mess = Message.objects.create(
            from_user = request.user,
            message = message,
            to_users = selected_users,
            seen_by = ""
        )
        mess.save()

    return render(request, "messages/create_announcement_view.html", {
        "customers" : customer_usernames
    })


def recent_messages(request):
    sent_messages = Message.objects.filter(from_user=request.user)
    for i in sent_messages:
        print(i.seen_by)
    return render(request, 'messages/recent_messages.html', {'messages': sent_messages})



def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, from_user=request.user)

    message.delete()
    return redirect('recent_messages')


def update_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, from_user=request.user)

    if request.method == 'POST':
        # Update the message text and recipients
        message_text = request.POST.get('message')
        selected_users = request.POST.getlist('selected_users')
        to_users = ",".join(selected_users)

        message.message = message_text
        message.to_users = to_users
        message.seen_by = ""
        message.sent = timezone.now()
        message.save()

        return redirect('recent_messages')

    customer_usernames = User.objects.filter(is_customer=True).values_list('username', flat=True)
    return render(request, 'messages/update_message.html', {'message': message, 'customer_usernames': customer_usernames})

def see_messages(request, user_id):
    user = User.objects.get(id=user_id)

    received_messages = Message.objects.filter(to_users__icontains=user.username)

    messages = received_messages

    return render(request, 'messages/see_messages.html', {'messages': messages})


def unreaden_messages(username):
    received_messages = Message.objects.filter(to_users__icontains=username)

    unread_messages = received_messages.exclude(seen_by__icontains=username)

    return unread_messages.exists()

def confirm_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    user = request.user
    seen_by_users = message.seen_by.split(',') if message.seen_by else []
    if user.username not in seen_by_users:
        seen_by_users.append(user.username)
        
        message.seen_by = ','.join(seen_by_users)
        message.save()

    return redirect('see_messages', request.user.id)