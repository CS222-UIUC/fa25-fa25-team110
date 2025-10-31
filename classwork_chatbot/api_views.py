from urllib.parse import urlencode
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

STREAMLIT_URL = "http://localhost:8501"

# Called after Google OAuth via django-allauth.
@login_required
def login_success(request):
    user = request.user
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    qp = urlencode({"access": str(access), "refresh": str(refresh)})
    return redirect(f"{STREAMLIT_URL}/?{qp}")

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    u = request.user
    return Response({
        "id": u.id,
        "email": u.email,
        "username": u.get_username(),
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def protected_data(request):
    return Response({"secret": f"Hello {request.user.get_username()}, this is protected."})

# SimpleJWT's refresh
@api_view(["POST"])
@permission_classes([AllowAny])
def token_refresh(request):
    """
    Proxy to SimpleJWT's refresh (expects {"refresh": "<token>"}).
    """
    view = TokenRefreshView.as_view()
    return view(request._request)  # pass Django request