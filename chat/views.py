from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt


class ChatPageView(TemplateView):
    template_name = "chat/index.html"


@csrf_exempt
@api_view(['POST'])
def chat_api(request):
    """A very small mock chat API so the frontend works immediately.

    This echoes the user's message. Replace or extend this with a real
    backend (OpenAI, other model endpoints) when available.
    """
    text = request.data.get('message') if hasattr(request, 'data') else None
    if text is None:
        return Response({'error': 'no message provided'}, status=400)

    reply = f"Echo: {text}"
    return Response({'reply': reply})
