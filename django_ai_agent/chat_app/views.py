from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import openai
from django.conf import settings

def chat_interface(request):
    """
    Render the chat interface
    """
    return render(request, 'chat/chat.html')

@csrf_exempt
def chat_api(request):
    """
    Handle chat API requests
    """
    if request.method == 'POST':
        try:
            # Parse the JSON data
            data = json.loads(request.body)
            message = data.get('message', '')
            
            # In a real implementation, you would integrate with an AI service
            # For now, we'll simulate a response
            response_text = f"I received your message: '{message}'. This is a simulated response from the AI assistant."
            
            # Return the response
            return JsonResponse({
                'status': 'success',
                'response': response_text
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    })
