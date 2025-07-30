
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseForbidden


class SuperUserOnlyMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login with ?next=
            return redirect_to_login(self.request.get_full_path())
        else:
            return HttpResponseForbidden("You do not have permission to access this.")
