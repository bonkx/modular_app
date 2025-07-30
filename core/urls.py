from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('module/', ModuleListView.as_view(), name='module_list'),
    path('module/install/<slug:slug>/', ModuleInstallView.as_view(), name='module_install'),
    path('module/upgrade/<slug:slug>/', ModuleUpgradeView.as_view(), name='module_upgrade'),
    path('module/uninstall/<slug:slug>/', ModuleUninstallView.as_view(), name='module_uninstall'),
]
