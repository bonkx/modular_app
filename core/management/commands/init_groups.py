from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Create default user groups: manager, user, public'

    def handle(self, *args, **kwargs):
        groups = ['manager', 'user', 'public']
        for name in groups:
            group, created = Group.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created group: {name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Group already exists: {name}"))
