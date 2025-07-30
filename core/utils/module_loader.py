import subprocess
from django.conf import settings

from core.models import ModuleRegistry

AVAILABLE_MODULES = getattr(settings, "AVAILABLE_MODULES", [])


def get_available_modules():
    return ModuleRegistry.objects.all()


def get_installed_modules():
    return ModuleRegistry.objects.filter(is_installed=True).values_list('slug', flat=True)


def run_management_command(*args):
    """
    Running the Django manage.py command.
    Example: run_management_command('migrate', 'app_name')

    Returns:
        True if successful (exit code 0), False if unsuccessful.
    """
    print(f"\n🚀 Running: python manage.py {' '.join(args)}")
    result = subprocess.run(['python', 'manage.py', *args, '--noinput'], capture_output=True, text=True)

    if result.returncode == 0:
        print("Command succeeded.")
        return True, result.stdout.strip()
    else:
        print("Command failed.")
        warning = result.stdout.strip()
        error = result.stderr.strip()
        if 'non-nullable field' in warning and 'without specifying a default' in warning:
            return False, warning
        return False, error


def install_module(slug):
    try:
        module = ModuleRegistry.objects.get(slug=slug)
    except ModuleRegistry.DoesNotExist:
        raise ValueError(f"Module with slug '{slug}' is not registered")

    if module.is_installed:
        return False  # already installed

    # Run makemigrations and migrate for module
    success, message = run_management_command('makemigrations', slug)

    if success:
        run_management_command('migrate', slug)
    else:
        # Return Failed
        raise ValueError(message)

    module.is_installed = True
    module.save()
    return module, True


def uninstall_module(slug):
    try:
        module = ModuleRegistry.objects.get(slug=slug)
    except ModuleRegistry.DoesNotExist:
        raise ValueError(f"Module with slug '{slug}' is not registered")

    module.is_installed = False
    module.save()

    # data in table still exists — only disabled
    return module, True


def upgrade_module(slug):
    try:
        module = ModuleRegistry.objects.get(slug=slug)

    except ModuleRegistry.DoesNotExist:
        raise ValueError(f"Module with slug '{slug}' is not registered")

    if not module.is_installed:
        raise ValueError("Module must be installed before upgrading")

    success, message = run_management_command('makemigrations', slug)

    if success:
        run_management_command('migrate', slug)

        # Update version
        old_version = module.version
        major, minor, patch = map(int, old_version.split('.'))
        module.version = f"{major}.{minor}.{patch + 1}"

        module.save()
    else:
        # Return Failed
        raise ValueError(message)

    return module, True
