from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    """
    Render the main index page
    """
    return render(request, 'frontend/index.html')

def dashboard(request):
    """
    Render the dashboard page
    """
    return render(request, 'frontend/dashboard.html')

def scan(request):
    """
    Render the scan page
    """
    return render(request, 'frontend/scan.html')

def results(request):
    """
    Render the results page
    """
    return render(request, 'frontend/results.html')

def reports(request):
    """
    Render the reports page
    """
    return render(request, 'frontend/reports.html')

def config(request):
    """
    Render the configuration page
    """
    return render(request, 'frontend/config.html')

@csrf_exempt
def api_scan(request):
    """
    Handle scan API requests
    """
    if request.method == 'POST':
        try:
            # Parse the JSON data
            data = json.loads(request.body)
            target = data.get('target', '')
            modules = data.get('modules', [])
            
            # In a real implementation, you would call the actual scanning modules
            # For now, we'll simulate a response
            response_data = {
                'status': 'success',
                'message': f'Scan started on {target} with modules: {", ".join(modules)}',
                'scan_id': '12345'
            }
            
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    })

def health_check(request):
    """
    Health check endpoint
    """
    return JsonResponse({
        'status': 'healthy',
        'message': 'AI Information Gathering Agent is running'
    })
