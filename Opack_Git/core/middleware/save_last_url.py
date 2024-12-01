class SaveLastVisitedURLMiddleware:
    """
    Middleware pour sauvegarder la dernière URL visitée par l'utilisateur,
    sauf si elle est une URL de déconnexion ou une URL administrative.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Ignore certaines URL (admin, logout, etc.)
        if request.path not in ['/logout/'] and not request.path.startswith('/admin/'):
            request.session['last_visited_url'] = request.path
        response = self.get_response(request)
        return response
