from django.http import HttpResponseForbidden, Http404
from core.models import ModuleRegistry


class ModuleAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/products/'):
            try:
                module = ModuleRegistry.objects.get(slug='product_module')
                if not module.is_installed:
                    raise Http404()
            except ModuleRegistry.DoesNotExist:
                raise Http404()

        return self.get_response(request)
