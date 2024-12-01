from core.models import Colis

def add_colis_to_context(request):
    if 'colis_id' in request.resolver_match.kwargs:
        colis_id = request.resolver_match.kwargs.get('colis_id')
        try:
            colis = Colis.objects.get(id=colis_id)
            return {'colis': colis}
        except Colis.DoesNotExist:
            pass
    return {}
