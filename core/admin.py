from django.contrib import admin
from .models import ModuleRegistry

# Register your models here.


@admin.register(ModuleRegistry)
class ModuleRegistryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'version', 'is_installed', 'landing_url')
    search_fields = ('name', 'slug')
    list_filter = ('is_installed',)
