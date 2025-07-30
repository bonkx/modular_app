from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command


class Command(BaseCommand):
    help = "Initialize default groups, users, and modules for the project."

    def handle(self, *args, **options):
        try:
            self.stdout.write(self.style.NOTICE("Running database migrations...\n"))
            call_command('migrate')

            self.stdout.write(self.style.NOTICE("\nStarting project setup..."))

            self.stdout.write(self.style.NOTICE("\nInitializing groups...\n"))
            call_command('init_groups')

            self.stdout.write(self.style.NOTICE("\nInitializing permissions...\n"))
            call_command('init_permissions')

            self.stdout.write(self.style.NOTICE("\nInitializing modules...\n"))
            call_command('init_modules')

            self.stdout.write(self.style.NOTICE("\nInitializing users...\n"))
            call_command('init_users')

            self.stdout.write(self.style.SUCCESS("\nProject setup completed successfully.\n"))

        except Exception as e:
            raise CommandError(f"Setup failed: {str(e)}")
