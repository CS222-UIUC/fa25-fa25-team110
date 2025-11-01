from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.ChatPageView.as_view(), name='chat_home'),
    path('api/chat/', views.chat_api, name='chat_api'),
]
