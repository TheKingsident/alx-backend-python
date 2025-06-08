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
        
class OffensiveLanguageMiddleware:
    "that tracks number of chat messages sent by each ip address and implement a time based limit i.e 5 messages per minutes such that if a user exceeds the limit, it blocks further messaging and returns and error"
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_count = {}
        self.time_window = 60
        self.message_limit = 5

    def __call__(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        current_time = datetime.now()

        # Initialize user message count if not present
        if ip_address not in self.message_count:
            self.message_count[ip_address] = []

        # Remove timestamps older than the time window
        self.message_count[ip_address] = [
            timestamp for timestamp in self.message_count[ip_address]
            if (current_time - timestamp).seconds < self.time_window
        ]

        # Check if user exceeded message limit
        if len(self.message_count[ip_address]) >= self.message_limit:
            return HttpResponse("Message limit exceeded. Try again later.", status=429)

        # Log the current message timestamp
        self.message_count[ip_address].append(current_time)

        response = self.get_response(request)
        return response
