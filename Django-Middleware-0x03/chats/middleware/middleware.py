import os
from datetime import datetime

from django.http import HttpResponse

class RequestLoggingMiddleware:
    """
    Middleware to log request details.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Set log file path relative to project root
        self.log_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'requests.log'
        )

    def __call__(self, request):
        user = request.user if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous'
        with open(self.log_path, 'a') as log_file:
            log_file.write(f"{datetime.now()} - User: {user} - Path: {request.path}\n")
        print(f"Request Method: {request.method}, Request Path: {request.path}")
        
        response = self.get_response(request)
        
        return response

class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to the application based on time.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if 18 <= current_hour < 21:  # Allow access only between 6 PM and 9 PM
            return self.get_response(request)
        else:
            return HttpResponse("Access restricted to business hours (6 PM - 9 PM).", status=403)