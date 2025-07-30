from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()


class Command(BaseCommand):
    help = 'Create default users and assign them to groups'

    def handle(self, *args, **kwargs):
        users_data = [
            {
                'username': 'admin',
                'email': 'admin@example.com',
                'password': 'admin123',
                'is_superuser': True,
                'is_staff': True,
                'group': None,
            },
            {
                'username': 'manager',
                'email': 'manager@example.com',
                'password': 'manager123',
                'is_superuser': False,
                'is_staff': True,
                'group': 'manager',
            },
            {
                'username': 'user',
                'email': 'user@example.com',
                'password': 'user123',
                'is_superuser': False,
                'is_staff': False,
                'group': 'user',
            },
        ]

        for user_data in users_data:
            username = user_data['username']
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f"User '{username}' already exists."))
                continue

            user = User.objects.create_user(
                username=username,
                email=user_data['email'],
                password=user_data['password'],
                is_superuser=user_data['is_superuser'],
                is_staff=user_data['is_staff']
            )

            if user_data['group']:
                group, _ = Group.objects.get_or_create(name=user_data['group'])

                user.groups.add(group)

                # Refresh permission cache
                user = User.objects.get(pk=user.pk)

                # (optional) Debug log
                print("User permissions:", user.get_all_permissions())

            self.stdout.write(self.style.SUCCESS(f"Created user '{username}'"))
