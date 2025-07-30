from django.core.management.base import BaseCommand
from core.models import ModuleRegistry

MODULES = [
    {
        'name': 'Product Module',
        'slug': 'product_module',
        "description": "Manages product data including name, barcode, price, and stock.",
        'version': '1.0.0',
        'is_installed': False,
        'landing_url': '/products/',
    },
]


class Command(BaseCommand):
    help = "Create default module registry entries."

    def handle(self, *args, **kwargs):
        for module in MODULES:
            obj, created = ModuleRegistry.objects.get_or_create(
                slug=module["slug"],
                defaults={
                    'name': module['name'],
                    'version': module['version'],
                    'is_installed': module['is_installed'],
                    'landing_url': module['landing_url'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created module '{obj.name}'"))
            else:
                self.stdout.write(self.style.WARNING(f"Module '{obj.name}' already exists."))
