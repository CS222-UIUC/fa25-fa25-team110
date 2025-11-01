from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import UserProfile


@api_view(["POST"])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")
    user_type = request.data.get("user_type", "student")

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username exists"}, status=400)

    user = User.objects.create_user(username=username, password=password, email=email)
    UserProfile.objects.create(user=user, user_type=user_type)

    return Response({"message": "User created", "user_type": user_type})


@api_view(["POST"])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        profile = UserProfile.objects.get(user=user)
        return Response({"username": user.username, "user_type": profile.user_type})
    return Response({"error": "Invalid credentials"}, status=401)
