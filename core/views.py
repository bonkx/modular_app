from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, TemplateView
from django.views import View

from .utils.module_loader import install_module, upgrade_module, uninstall_module
from .models import ModuleRegistry
from .mixins import SuperUserOnlyMixin

# Create your views here.


class HomeView(TemplateView):
    template_name = 'core/home.html'


class ModuleListView(SuperUserOnlyMixin, ListView):
    model = ModuleRegistry
    template_name = 'core/module_list.html'
    context_object_name = 'modules'


class ModuleInstallView(SuperUserOnlyMixin, View):
    def post(self, request, slug):
        try:
            module, installed = install_module(slug)
            if installed:
                messages.success(request, f"{module.name} installed.")
            else:
                messages.info(request, f"{module.name} is already installed.")
        except ValueError as e:
            messages.error(request, str(e))

        return redirect('module_list')


class ModuleUpgradeView(SuperUserOnlyMixin, View):
    def post(self, request, slug):
        try:
            module, upgraded = upgrade_module(slug)
            if upgraded:
                messages.success(request, f"{module.name} upgraded.")
        except ValueError as e:
            messages.error(request, str(e))

        return redirect('module_list')


class ModuleUninstallView(SuperUserOnlyMixin, View):
    def post(self, request, slug):
        try:
            module, uninstalled = uninstall_module(slug)
            if uninstalled:
                messages.success(request, f"{module.name} uninstalled.")
        except ValueError as e:
            messages.error(request, str(e))

        return redirect('module_list')
