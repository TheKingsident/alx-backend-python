import os
from datetime import datetime

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