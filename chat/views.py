from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.
from chat.models import Thread


@login_required
def messages_page(request):
    users = User.objects.all()

    for user in users:
        if request.user != user:
            try:
                thread = Thread.objects.get(first_person=request.user, second_person=user)
                print(thread)
            except:
                try:
                    thread = Thread(first_person=request.user, second_person=user)
                    thread2 = Thread.objects.get(first_person=user, second_person=request.user)
                except:
                    thread.save()
                    pass
                pass


    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    context = {
        'Threads': threads
    }
    return render(request, 'main/messages.html', context)

