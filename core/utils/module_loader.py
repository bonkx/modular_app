import os
import subprocess
from django.conf import settings
from pathlib import Path

from core.models import ModuleRegistry


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

    # --- Find the path to manage.py relatively ---
    # For example, this file is stored in the project root or one level above manage.py.
    BASE_DIR = Path(__file__).resolve().parent

    # Loop up until you find manage.py
    while not (BASE_DIR / 'manage.py').exists() and BASE_DIR != BASE_DIR.parent:
        BASE_DIR = BASE_DIR.parent

    if not (BASE_DIR / 'manage.py').exists():
        raise FileNotFoundError("manage.py not found in parent directories.")

    print(f"\n🚀 Running: python manage.py {' '.join(args)}")

    command = ['python', 'manage.py', *args, '--noinput']
    result = subprocess.run(
        command,
        cwd=str(BASE_DIR),
        capture_output=True,
        text=True
    )

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
