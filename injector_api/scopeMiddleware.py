from .container import container
class ScopeMiddleware:
    """
        Middleware that ensures a new scope is started at the beginning of a web request and ended at the end.
    """
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        container.start_scope()
        try:
            response = self.handle_request(request, *args, **kwargs)
        finally:
            container.end_scope()
        return response

    def handle_request(self, request, *args, **kwargs):
        if self.get_response:
            return self.get_response(request)
        return None  
    
    
class ScoperMiddlewareManual:
    
    @staticmethod
    def start(*funcs)->None:
        container.start_scope()
        try:
            for func in funcs:
                func()
        finally:
            container.end_scope()
    
        
        
        
        
