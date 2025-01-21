from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import SignupForm
from django.http import JsonResponse
from .models import Message
from django.contrib.auth.models import User

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'chat/signup.html', {'form': form})

@csrf_exempt
def save_message(request):
    if request.method == 'POST':
        message_content = request.POST.get('message')
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        message = Message.objects.create(user=user, content=message_content)
        return JsonResponse({'status': 'success', 'message_id': message.id}, status=200)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def chat_view(request):
    # messages = Message.objects.all()
    messages = Message.objects.all().order_by('timestamp')[:20]  # Get the last 20 messages
    return render(request, 'chat/chat.html', {'messages': messages})
