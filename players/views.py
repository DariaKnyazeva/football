from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic.list import ListView

from .models import Player
from .forms import PlayerForm


class RegistractionView(FormView):
    template_name = 'players_registration.html'
    form_class = PlayerForm
    success_url = '/'

    def form_valid(self, form):

        # TODO: form.send_email()
        return super().form_valid(form)


class CoachViewMixin:
    def dispatch(self, *args, **kwargs):
        # TODO: who has perms to manage players? Is it true that all players are for coaches only to manage?
        if not self.request.user.is_coach:
            raise PermissionDenied
        return super().dispatch(*args, **kwargs)


class PlayerListView(CoachViewMixin, ListView):
    model = Player
    template_name = 'player_list.html'
    paginate_by = settings.RESULTS_PER_PAGE

    def get_queryset(self):
        return Player.objects.all()


class PlayerCreateView(CoachViewMixin, CreateView):
    model = Player
    form_class = PlayerForm
    template_name = 'base/form_page.html'

    def get_success_url(self):
        return reverse('player_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Add Player"
        return context

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save()
        messages.add_message(self.request, messages.SUCCESS, 'Player has been created.')
        return HttpResponseRedirect(self.get_success_url())


class PlayerEditView(CoachViewMixin, UpdateView):
    model = Player
    pk_url_kwarg = 'player_id'
    form_class = PlayerForm
    template_name = 'base/form_page.html'

    def get_success_url(self):
        return reverse('player_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Edit Player"
        return context

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save()
        messages.add_message(self.request, messages.SUCCESS, 'Player has been updated.')
        return HttpResponseRedirect(self.get_success_url())
