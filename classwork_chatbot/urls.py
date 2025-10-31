"""
URL configuration for classwork_chatbot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api import views as api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # adds all Google OAuth routes

    # after allauth, mint JWTs and go to Streamlit with tokens
    path('login/success/', api_views.login_success, name='login-success'),

    # protected endpoints and token refresh
    path('api/me/', api_views.me),
    path('api/protected-data/', api_views.protected_data),
    path('api/token/refresh/', api_views.token_refresh),
]
