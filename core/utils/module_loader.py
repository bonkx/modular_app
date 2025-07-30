import subprocess
from django.conf import settings

from core.models import ModuleRegistry

AVAILABLE_MODULES = getattr(settings, "AVAILABLE_MODULES", [])


def get_available_modules():
    return ModuleRegistry.objects.all()


def get_installed_modules():
    return ModuleRegistry.objects.filter(is_installed=True).values_list('slug', flat=True)


def install_module(slug):
    try:
        module = ModuleRegistry.objects.get(slug=slug)
    except ModuleRegistry.DoesNotExist:
        raise ValueError(f"Module with slug '{slug}' is not registered")

    if module.is_installed:
        return False  # already installed

    # Jalankan makemigrations dan migrate untuk module tersebut
    subprocess.call(['python', 'manage.py', 'makemigrations', slug])
    subprocess.call(['python', 'manage.py', 'migrate', slug])

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

    # tabel data tetap ada — hanya dinonaktifkan
    return module, True


def upgrade_module(slug):
    try:
        module = ModuleRegistry.objects.get(slug=slug)
        # Update version
        old_version = module.version
        major, minor, patch = map(int, old_version.split('.'))
        module.version = f"{major}.{minor}.{patch + 1}"

        module.save()
    except ModuleRegistry.DoesNotExist:
        raise ValueError(f"Module with slug '{slug}' is not registered")

    if not module.is_installed:
        raise ValueError("Module must be installed before upgrading")

    subprocess.call(['python', 'manage.py', 'makemigrations', slug])
    subprocess.call(['python', 'manage.py', 'migrate', slug])

    return module, True
