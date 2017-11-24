from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from .models import Player
from .forms import RegistractionForm


class RegistractionView(FormView):
    template_name = 'players_registration.html'
    form_class = RegistractionForm
    success_url = '/'

    def form_valid(self, form):

        # TODO: form.send_email()
        return super().form_valid(form)


class PlayerListView(ListView):
    model = Player
    template_name = 'player_list.html'
    paginate_by = settings.RESULTS_PER_PAGE

    def get_queryset(self):
        return Player.objects.all()

    def dispatch(self, *args, **kwargs):
        # TODO: who has perms to see all players? Is it true that all players are for coaches only to see?
        if not self.request.user.is_coach:
            raise PermissionDenied
        return super().dispatch(*args, **kwargs)
