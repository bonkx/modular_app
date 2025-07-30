from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from product_module.models import Product


class Command(BaseCommand):
    help = "Initialize product permissions for manager, user, and public groups."

    def handle(self, *args, **options):
        # Map group to permission codes
        permission_map = {
            "manager": ["add", "change", "delete", "view"],
            "user": ["add", "change", "view"],
            "public": ["view"],
        }

        content_type = ContentType.objects.get_for_model(Product)

        for group_name, actions in permission_map.items():
            group, created = Group.objects.get_or_create(name=group_name)
            for action in actions:
                codename = f"{action}_product"
                try:
                    permission = Permission.objects.get(codename=codename, content_type=content_type)
                    group.permissions.add(permission)
                    self.stdout.write(f"Permission '{codename}' added to group '{group_name}'")
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Permission '{codename}' not found"))

        self.stdout.write(self.style.SUCCESS("Product permissions initialized successfully."))
