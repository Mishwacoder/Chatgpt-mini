from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Chat,UserProfile
import json
from django.core.serializers import serialize
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Chat
from django.utils import timezone
from django.db.models import Q
import base64
from django.shortcuts import get_object_or_404
from decouple import config

API_KEY = config('GEMINI_API_KEY')
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"



@csrf_exempt
def chatbot_response(request):
    chats=Chat.objects.filter(user=request.user)
    if request.method == "POST":
        try:
            # Parse user input from request
            data = json.loads(request.body)
            user_message = data.get("message", "")

            if not user_message:
                return JsonResponse({"error": "Empty message"}, status=400)

            # Prepare API request payload
            payload = {
                "contents": [{
                    "role": "user",
                    "parts": [{"text": user_message}]
                }]
            }

            # Send request to Gemini API
            response = requests.post(API_URL, json=payload, headers={"Content-Type": "application/json"})
            api_data = response.json()

            # Extract the chatbot's response
            chatbot_response = api_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

            chat=Chat(user=request.user, message=user_message,response=chatbot_response,timestamp=timezone.now)
            chat.save()

            return JsonResponse({"response": chatbot_response})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@login_required(login_url='login')
def home(request):
    query = request.GET.get('q', '')
    chats = Chat.objects.filter(user=request.user).order_by('-timestamp')
    if query:
        chats = chats.filter(
            Q(message__icontains=query) | Q(response__icontains=query)
        )

    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    chats_json = json.dumps([
        {
            'id': chat.id,
            'message': chat.message,
            'response': chat.response,
            'timestamp': chat.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
        for chat in chats
    ])
    return render(request, "base/home.html", {'chats': chats, 'chats_json': chats_json,'profile': profile,'query': query})
@csrf_exempt
@login_required(login_url='login')
def process_image(request):
    if request.method == 'POST':
        image_file = request.FILES.get('image')
        user_prompt = request.POST.get('prompt', '').strip()

        # If both are missing, show error
        if not image_file and not user_prompt:
            messages.error(request, "Please provide a prompt or upload an image.")
            return redirect('home')

        parts = []

        if image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
            parts.append({
                "inline_data": {
                    "mime_type": image_file.content_type,
                    "data": image_data
                }
            })

        if user_prompt:
            parts.append({
                "text": user_prompt
            })
        elif not image_file:
            parts.append({
                "text": "Describe this image."
            })

        payload = {
            "contents": [{
                "role": "user",
                "parts": parts
            }]
        }

        try:
            response = requests.post(API_URL, json=payload, headers={"Content-Type": "application/json"})
            api_data = response.json()
            bot_reply = api_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        except Exception as e:
            bot_reply = f"Error analyzing input: {str(e)}"

        Chat.objects.create(
            user=request.user,
            message=user_prompt if user_prompt else "[Image uploaded]",
            response=bot_reply,
            timestamp=timezone.now()
        )

        return redirect('home')

    return redirect('home')

def delete_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, user=request.user)
    chat.delete()
    return redirect('home')

def user_register(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password')
        cpass = request.POST.get('cpassword')
        profile_pic = request.FILES.get('profile_pic')

        # Validate form fields
        if not uname or not email or not pass1 or not cpass:
            messages.error(request, "All fields are required.")
            return redirect('register')

        # Check if passwords match
        if pass1 != cpass:
            messages.error(request, "Passwords do not match. Please try again.")
            return redirect('register')

        # Check if username already exists
        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already taken. Choose another.")
            return redirect('register')

        # Create and save new user
        my_user = User.objects.create_user(username=uname, email=email, password=pass1)
        my_user.save()

        UserProfile.objects.create(user=my_user, profile_pic=profile_pic)  # Save uploaded pic

        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')

    return render(request, "custadmin/register.html")

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')  
        password = request.POST.get('password')  
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request,user)
            return redirect('home')  
        else:
            print("Authentication failed: Incorrect username or password.")
        
    return render(request, "custadmin/login.html")

def logoutpg(request):
    logout(request)
    return redirect('login')